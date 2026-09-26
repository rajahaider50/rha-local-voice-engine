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
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import java.io.IOException
import java.util.concurrent.TimeUnit

class RhaVoiceService : Service() {
    
    private val CHANNEL_ID = "RhaVoiceChannel"
    private var wakeLock: PowerManager.WakeLock? = null
    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        acquireWakeLock()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val notification = createNotification()
        startForeground(1, notification)
        
        // Simulating Audio Recording and sending to FastAPI server
        // In full production, use AudioRecord here to capture mic stream
        sendAudioToServer(ByteArray(32000)) // Sending empty 1-second 16kHz chunk as test

        return START_STICKY
    }
    
    private fun sendAudioToServer(audioData: ByteArray) {
        // Assume the Python FastAPI server is running on Termux (127.0.0.1:8000)
        val url = "http://127.0.0.1:8000/api/v1/voice"
        
        val requestBody = MultipartBody.Builder()
            .setType(MultipartBody.FORM)
            .addFormDataPart(
                "audio", "voice.wav",
                RequestBody.create("application/octet-stream".toMediaTypeOrNull(), audioData)
            )
            .build()
            
        val request = Request.Builder()
            .url(url)
            .post(requestBody)
            .build()
            
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                println("RHA Server Connection Failed: ${e.message}")
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    val responseBody = response.body?.string()
                    println("RHA Server Response: $responseBody")
                    // Process Intent (e.g. Open App) here based on response JSON
                }
            }
        })
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
            .setContentTitle("RHA Engine Connected")
            .setContentText("Listening and streaming to Local Server...")
            .setSmallIcon(android.R.drawable.sym_def_app_icon)
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
        wakeLock?.release()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null
    }
}
