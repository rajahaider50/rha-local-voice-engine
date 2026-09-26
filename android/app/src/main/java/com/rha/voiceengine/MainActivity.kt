package com.rha.voiceengine

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
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
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = Color(0xFF121212) // Premium Dark Mode
                ) {
                    VoiceAssistantScreen(
                        onStartEngine = {
                            val intent = Intent(this, RhaVoiceService::class.java)
                            startForegroundService(intent)
                        },
                        onStopEngine = {
                            val intent = Intent(this, RhaVoiceService::class.java)
                            stopService(intent)
                        }
                    )
                }
            }
        }
    }
}

@Composable
fun RhaTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = Color(0xFF00E676),
            background = Color(0xFF121212),
            surface = Color(0xFF1E1E1E)
        ),
        content = content
    )
}

@Composable
fun VoiceAssistantScreen(onStartEngine: () -> Unit, onStopEngine: () -> Unit) {
    var isListening by remember { mutableStateOf(false) }
    var statusText by remember { mutableStateOf("IDLE") }
    
    // Premium pulsing animation for the voice button
    val infiniteTransition = rememberInfiniteTransition()
    val pulseScale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = if (isListening) 1.2f else 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        )
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.SpaceBetween
    ) {
        // Header
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text(
                text = "RHA ENGINE",
                color = Color.White,
                fontSize = 28.sp,
                fontWeight = FontWeight.Bold,
                letterSpacing = 2.sp
            )
            Text(
                text = "100% Local AI",
                color = Color.Gray,
                fontSize = 14.sp
            )
        }

        // Voice Orb
        Box(
            modifier = Modifier
                .size(200.dp)
                .scale(pulseScale)
                .clip(CircleShape)
                .background(
                    if (isListening) Color(0xFF00E676).copy(alpha = 0.2f) 
                    else Color.DarkGray.copy(alpha = 0.3f)
                ),
            contentAlignment = Alignment.Center
        ) {
            Box(
                modifier = Modifier
                    .size(140.dp)
                    .clip(CircleShape)
                    .background(
                        if (isListening) Color(0xFF00E676) else Color.DarkGray
                    )
            )
        }

        // Status Text
        Text(
            text = statusText,
            color = if (isListening) Color(0xFF00E676) else Color.Gray,
            fontSize = 18.sp,
            fontWeight = FontWeight.Medium,
            letterSpacing = 1.sp
        )

        // Controls
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            Button(
                onClick = { 
                    isListening = true
                    statusText = "LISTENING"
                    onStartEngine()
                },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF1E1E1E))
            ) {
                Text("START ENGINE", color = Color.White)
            }
            
            Button(
                onClick = { 
                    isListening = false
                    statusText = "OFFLINE"
                    onStopEngine()
                },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFB00020))
            ) {
                Text("STOP", color = Color.White)
            }
        }
    }
}
