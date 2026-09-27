package com.rha.voiceengine

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.Bundle
import android.provider.Settings
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
    
    private val stateReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            val state = intent?.getStringExtra("state") ?: "IDLE"
            // Update global state object or ViewModel here in a full app
            // For now, we rely on the button press logic, but this is hooked up.
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        registerReceiver(stateReceiver, IntentFilter("RHA_STATE_UPDATE"))
        
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
    
    override fun onDestroy() {
        unregisterReceiver(stateReceiver)
        super.onDestroy()
    }
}

@Composable
fun RhaTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = Color(0xFF0A4FBF), // Premium RHA Blue
            background = Color(0xFF0A0A0A),
            surface = Color(0xFF121212)
        ),
        content = content
    )
}

@Composable
fun MainAppNav(onStartEngine: () -> Unit, onStopEngine: () -> Unit, context: Context) {
    var currentScreen by remember { mutableStateOf("HOME") }
    
    val sharedPref = context.getSharedPreferences("RhaPrefs", Context.MODE_PRIVATE)
    var serverIp by remember { mutableStateOf(sharedPref.getString("SERVER_IP", "127.0.0.1") ?: "127.0.0.1") }
    var serverPort by remember { mutableStateOf(sharedPref.getString("SERVER_PORT", "8000") ?: "8000") }

    Scaffold(
        bottomBar = {
            NavigationBar(containerColor = Color(0xFF121212)) {
                NavigationBarItem(
                    selected = currentScreen == "HOME",
                    onClick = { currentScreen = "HOME" },
                    icon = { Text("Assist", fontSize = 12.sp) },
                    label = { Text("Home") }
                )
                NavigationBarItem(
                    selected = currentScreen == "SERVER",
                    onClick = { currentScreen = "SERVER" },
                    icon = { Text("Net", fontSize = 12.sp) },
                    label = { Text("Server") }
                )
                NavigationBarItem(
                    selected = currentScreen == "PERMS",
                    onClick = { currentScreen = "PERMS" },
                    icon = { Text("Set", fontSize = 12.sp) },
                    label = { Text("Access") }
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
                "PERMS" -> PermissionsScreen(context)
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
            Text("RHA ENGINE", color = Color.White, fontSize = 28.sp, fontWeight = FontWeight.Bold, letterSpacing = 2.sp)
            Spacer(Modifier.height(4.dp))
            Text("ws://$serverAddress", color = Color.Gray, fontSize = 12.sp)
        }

        Box(
            modifier = Modifier
                .size(220.dp)
                .scale(pulseScale)
                .clip(CircleShape)
                .background(if (isListening) Color(0xFF0A4FBF).copy(alpha = 0.15f) else Color.DarkGray.copy(alpha = 0.1f)),
            contentAlignment = Alignment.Center
        ) {
            Box(
                modifier = Modifier
                    .size(150.dp)
                    .clip(CircleShape)
                    .background(if (isListening) Color(0xFF0A4FBF) else Color(0xFF1E1E1E))
            )
        }

        Text(statusText, color = if (isListening) Color(0xFF42A5F5) else Color.Gray, fontSize = 18.sp, fontWeight = FontWeight.Medium)

        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
            Button(
                onClick = { isListening = true; statusText = "LISTENING"; onStartEngine() },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0A4FBF)),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier.weight(1f).padding(end = 8.dp)
            ) { Text("CONNECT", color = Color.White, fontWeight = FontWeight.Bold) }
            
            Button(
                onClick = { isListening = false; statusText = "IDLE"; onStopEngine() },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF333333)),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier.weight(1f).padding(start = 8.dp)
            ) { Text("DISCONNECT", color = Color.White, fontWeight = FontWeight.Bold) }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ServerScreen(currentIp: String, currentPort: String, onSave: (String, String) -> Unit) {
    var ip by remember { mutableStateOf(currentIp) }
    var port by remember { mutableStateOf(currentPort) }

    Column(modifier = Modifier.fillMaxSize().padding(24.dp)) {
        Text("SERVER CONFIGURATION", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(32.dp))
        
        OutlinedTextField(
            value = ip,
            onValueChange = { ip = it },
            label = { Text("IPv4 Address", color = Color.Gray) },
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
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0A4FBF))
        ) {
            Text("SAVE & APPLY", color = Color.White, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun PermissionsScreen(context: Context) {
    Column(modifier = Modifier.fillMaxSize().padding(24.dp)) {
        Text("ACCESS CENTER", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(24.dp))
        
        Card(
            modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
            colors = CardDefaults.cardColors(containerColor = Color(0xFF1A1A1A))
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Automation Service", color = Color.White, fontWeight = FontWeight.Bold)
                Text("Required for clicking UI elements during voice commands.", color = Color.Gray, fontSize = 12.sp)
                Spacer(Modifier.height(12.dp))
                Button(
                    onClick = { 
                        val intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)
                        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK
                        context.startActivity(intent)
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF42A5F5))
                ) {
                    Text("OPEN SETTINGS", color = Color.Black)
                }
            }
        }
    }
}
