package com.rha.voiceengine

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.IBinder
import android.os.PowerManager
import androidx.core.app.NotificationCompat
import okhttp3.*
import okio.ByteString
import okio.ByteString.Companion.toByteString
import org.json.JSONObject
import java.util.concurrent.TimeUnit

import android.speech.tts.TextToSpeech
import java.util.Locale

class RhaVoiceService : Service(), TextToSpeech.OnInitListener {
    
    private val CHANNEL_ID = "RhaVoiceChannel"
    private var wakeLock: PowerManager.WakeLock? = null
    private var webSocket: WebSocket? = null
    private var tts: TextToSpeech? = null
    
    private val client = OkHttpClient.Builder()
        .pingInterval(10, TimeUnit.SECONDS)
        .build()

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        acquireWakeLock()
        tts = TextToSpeech(this, this)
        connectWebSocket()
    }

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            tts?.language = Locale("ur", "PK") // Default to Urdu, can fallback to English
        }
    }

    private var isRecording = false
    private var audioRecord: android.media.AudioRecord? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val notification = createNotification()
        startForeground(1, notification)
        
        startAudioRecording()

        return START_STICKY
    }
    
    private fun startAudioRecording() {
        if (androidx.core.content.ContextCompat.checkSelfPermission(this, android.Manifest.permission.RECORD_AUDIO) 
            != android.content.pm.PackageManager.PERMISSION_GRANTED) {
            println("Microphone permission not granted!")
            return
        }

        val sampleRate = 16000
        val channelConfig = android.media.AudioFormat.CHANNEL_IN_MONO
        val audioFormat = android.media.AudioFormat.ENCODING_PCM_16BIT
        val bufferSize = android.media.AudioRecord.getMinBufferSize(sampleRate, channelConfig, audioFormat)

        audioRecord = android.media.AudioRecord(
            android.media.MediaRecorder.AudioSource.MIC,
            sampleRate, channelConfig, audioFormat, bufferSize
        )

        audioRecord?.startRecording()
        isRecording = true

        Thread {
            val audioBuffer = ByteArray(bufferSize)
            while (isRecording) {
                val readResult = audioRecord?.read(audioBuffer, 0, bufferSize) ?: 0
                if (readResult > 0) {
                    val actualData = audioBuffer.copyOfRange(0, readResult)
                    webSocket?.send(actualData.toByteString())
                }
            }
        }.start()
    }

    private fun stopAudioRecording() {
        isRecording = false
        audioRecord?.stop()
        audioRecord?.release()
        audioRecord = null
    }
    
    private fun connectWebSocket() {
        val sharedPref = getSharedPreferences("RhaPrefs", Context.MODE_PRIVATE)
        val ip = sharedPref.getString("SERVER_IP", "127.0.0.1")
        val port = sharedPref.getString("SERVER_PORT", "8000")
        val url = "ws://$ip:$port/ws/voice"
        
        val request = Request.Builder().url(url).build()
        
        webSocket = client.newWebSocket(request, object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                println("RHA WebSocket Connected")
            }

            override fun onMessage(webSocket: WebSocket, text: String) {
                println("RHA Server Message: $text")
                try {
                    val json = JSONObject(text)
                    when (json.getString("type")) {
                        "command" -> handleCommand(json)
                        "state" -> broadcastState(json.getString("value"))
                        "transcription" -> println("Transcribed: ${json.getString("text")}")
                        "llm_token" -> {
                            val msg = json.getString("text")
                            println("LLM: $msg")
                        }
                        "tts" -> {
                            val speakText = json.getString("text")
                            tts?.speak(speakText, TextToSpeech.QUEUE_ADD, null, null)
                        }
                        "interrupt" -> {
                            tts?.stop()
                        }
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }

            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                println("RHA WebSocket Failed: ${t.message}")
            }
        })
    }

    private fun handleCommand(json: JSONObject) {
        val action = json.getString("action")
        when (action) {
            "OPEN_APP" -> {
                val packageName = json.optString("package", "")
                if (packageName.isNotEmpty()) {
                    val launchIntent = packageManager.getLaunchIntentForPackage(packageName)
                    if (launchIntent != null) {
                        launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        startActivity(launchIntent)
                    } else {
                        println("App not found: $packageName")
                    }
                }
            }
            "WEB_SEARCH" -> {
                val query = json.optString("query", "")
                if (query.isNotEmpty()) {
                    val intent = Intent(Intent.ACTION_WEB_SEARCH)
                    intent.putExtra(android.app.SearchManager.QUERY, query)
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    try {
                        startActivity(intent)
                    } catch (e: Exception) {
                        println("No browser found for web search")
                    }
                }
            }
        }
    }
    
    private fun broadcastState(state: String) {
        // Send state back to MainActivity UI
        val intent = Intent("RHA_STATE_UPDATE")
        intent.putExtra("state", state)
        sendBroadcast(intent)
    }

    private fun acquireWakeLock() {
        val powerManager = getSystemService(Context.POWER_SERVICE) as PowerManager
        wakeLock = powerManager.newWakeLock(
            PowerManager.PARTIAL_WAKE_LOCK,
            "RHAVoiceEngine::BackgroundListening"
        )
        wakeLock?.acquire()
    }

    private fun createNotification(): Notification {
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("RHA Engine Active")
            .setContentText("Connected to AI Server via WebSocket")
            .setSmallIcon(R.mipmap.ic_launcher)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val serviceChannel = NotificationChannel(
                CHANNEL_ID,
                "RHA Engine Background Service",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(serviceChannel)
        }
    }

    override fun onDestroy() {
        tts?.stop()
        tts?.shutdown()
        stopAudioRecording()
        webSocket?.close(1000, "Service destroyed")
        wakeLock?.release()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null
    }
}
