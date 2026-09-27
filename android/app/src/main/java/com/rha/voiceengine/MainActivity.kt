package com.rha.voiceengine

import android.content.Context
import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            RhaTheme {
                MainAppNav(
                    onStartEngine = {
                        val intent = Intent(this, RhaVoiceService::class.java)
                        startForegroundService(intent)
                    },
                    onStopEngine = {
                        val intent = Intent(this, RhaVoiceService::class.java)
                        stopService(intent)
                    },
                    context = this
                )
            }
        }
    }
}

@Composable
fun RhaTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = Color(0xFF00E676),
            background = Color(0xFF0A0A0A),
            surface = Color(0xFF1A1A1A)
        ),
        content = content
    )
}

@Composable
fun MainAppNav(onStartEngine: () -> Unit, onStopEngine: () -> Unit, context: Context) {
    var currentScreen by remember { mutableStateOf("HOME") }
    
    // Shared Preferences for Server IP
    val sharedPref = context.getSharedPreferences("RhaPrefs", Context.MODE_PRIVATE)
    var serverIp by remember { mutableStateOf(sharedPref.getString("SERVER_IP", "127.0.0.1") ?: "127.0.0.1") }
    var serverPort by remember { mutableStateOf(sharedPref.getString("SERVER_PORT", "8000") ?: "8000") }

    Scaffold(
        bottomBar = {
            NavigationBar(containerColor = Color(0xFF121212)) {
                NavigationBarItem(
                    selected = currentScreen == "HOME",
                    onClick = { currentScreen = "HOME" },
                    icon = { Text("🏠") },
                    label = { Text("Home") }
                )
                NavigationBarItem(
                    selected = currentScreen == "SERVER",
                    onClick = { currentScreen = "SERVER" },
                    icon = { Text("🌐") },
                    label = { Text("Server") }
                )
                NavigationBarItem(
                    selected = currentScreen == "MODELS",
                    onClick = { currentScreen = "MODELS" },
                    icon = { Text("🧠") },
                    label = { Text("Models") }
                )
            }
        }
    ) { paddingValues ->
        Box(modifier = Modifier.padding(paddingValues).fillMaxSize()) {
            when (currentScreen) {
                "HOME" -> VoiceAssistantScreen(onStartEngine, onStopEngine, "$serverIp:$serverPort")
                "SERVER" -> ServerScreen(serverIp, serverPort, onSave = { ip, port -> 
                    serverIp = ip
                    serverPort = port
                    sharedPref.edit().putString("SERVER_IP", ip).putString("SERVER_PORT", port).apply()
                })
                "MODELS" -> ModelsScreen()
            }
        }
    }
}

@Composable
fun VoiceAssistantScreen(onStartEngine: () -> Unit, onStopEngine: () -> Unit, serverAddress: String) {
    var isListening by remember { mutableStateOf(false) }
    var statusText by remember { mutableStateOf("IDLE") }
    
    val infiniteTransition = rememberInfiniteTransition()
    val pulseScale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = if (isListening) 1.15f else 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(1200, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        )
    )

    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.SpaceBetween
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text("RHA ENGINE", color = Color.White, fontSize = 28.sp, fontWeight = FontWeight.Bold)
            Text("Target: http://$serverAddress", color = Color.Gray, fontSize = 12.sp)
        }

        Box(
            modifier = Modifier
                .size(220.dp)
                .scale(pulseScale)
                .clip(CircleShape)
                .background(if (isListening) Color(0xFF00E676).copy(alpha = 0.15f) else Color.DarkGray.copy(alpha = 0.2f)),
            contentAlignment = Alignment.Center
        ) {
            Box(
                modifier = Modifier
                    .size(150.dp)
                    .clip(CircleShape)
                    .background(if (isListening) Color(0xFF00E676) else Color(0xFF2A2A2A))
            )
        }

        Text(statusText, color = if (isListening) Color(0xFF00E676) else Color.Gray, fontSize = 18.sp, fontWeight = FontWeight.Medium)

        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
            Button(
                onClick = { isListening = true; statusText = "LISTENING"; onStartEngine() },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00E676)),
                shape = RoundedCornerShape(12.dp)
            ) { Text("START", color = Color.Black, fontWeight = FontWeight.Bold) }
            
            Button(
                onClick = { isListening = false; statusText = "OFFLINE"; onStopEngine() },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFB00020)),
                shape = RoundedCornerShape(12.dp)
            ) { Text("STOP", color = Color.White, fontWeight = FontWeight.Bold) }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ServerScreen(currentIp: String, currentPort: String, onSave: (String, String) -> Unit) {
    var ip by remember { mutableStateOf(currentIp) }
    var port by remember { mutableStateOf(currentPort) }

    Column(modifier = Modifier.fillMaxSize().padding(24.dp)) {
        Text("SERVER CONNECTION", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(8.dp))
        Text("Connect to Local AI Python Server", color = Color.Gray, fontSize = 14.sp)
        Spacer(Modifier.height(32.dp))
        
        OutlinedTextField(
            value = ip,
            onValueChange = { ip = it },
            label = { Text("Server IP Address", color = Color.Gray) },
            colors = TextFieldDefaults.colors(
                focusedTextColor = Color.White,
                unfocusedTextColor = Color.White,
                focusedContainerColor = Color.Transparent,
                unfocusedContainerColor = Color.Transparent
            ),
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(16.dp))
        OutlinedTextField(
            value = port,
            onValueChange = { port = it },
            label = { Text("Port", color = Color.Gray) },
            colors = TextFieldDefaults.colors(
                focusedTextColor = Color.White,
                unfocusedTextColor = Color.White,
                focusedContainerColor = Color.Transparent,
                unfocusedContainerColor = Color.Transparent
            ),
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(32.dp))
        
        Button(
            onClick = { onSave(ip, port) },
            modifier = Modifier.fillMaxWidth().height(50.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00E676))
        ) {
            Text("SAVE CONFIGURATION", color = Color.Black, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun ModelsScreen() {
    Column(modifier = Modifier.fillMaxSize().padding(24.dp)) {
        Text("MODEL MANAGER", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(24.dp))
        ModelItem("Whisper STT", "tiny.en", "ON SERVER")
        ModelItem("Qwen LLM", "1.5B Q4_K_M", "ON SERVER")
        ModelItem("openWakeWord", "hey_rha", "ON SERVER")
        ModelItem("Silero VAD", "v4.0", "ON SERVER")
    }
}

@Composable
fun ModelItem(name: String, details: String, status: String) {
    Card(
        modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF1E1E1E))
    ) {
        Row(
            modifier = Modifier.padding(16.dp).fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column {
                Text(name, color = Color.White, fontWeight = FontWeight.Bold)
                Text(details, color = Color.Gray, fontSize = 12.sp)
            }
            Text(status, color = Color(0xFF00E676), fontSize = 12.sp, fontWeight = FontWeight.Bold)
        }
    }
}
