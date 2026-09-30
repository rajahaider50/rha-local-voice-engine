package com.rha.voiceengine

import android.Manifest
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.compose.setContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private val Ink = Color(0xFF0B1020)
private val Navy = Color(0xFF111A36)
private val Purple = Color(0xFF7C5CFC)
private val Aqua = Color(0xFF39D8C5)
private val Muted = Color(0xFF8992AE)
private val Card = Color(0xFF182241)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { RhaConnectApp() }
    }
}

@Composable fun RhaConnectApp() {
    var loggedIn by remember { mutableStateOf(false) }
    RhaTheme { if (!loggedIn) LoginScreen { loggedIn = true } else HomeShell() }
}

@Composable private fun RhaTheme(content: @Composable () -> Unit) {
    MaterialTheme(colorScheme = darkColorScheme(primary = Purple, secondary = Aqua, background = Ink, surface = Card, onBackground = Color.White, onSurface = Color.White), content = content)
}

@Composable private fun LoginScreen(onContinue: () -> Unit) {
    Box(Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(Color(0xFF161A3E), Ink)))) {
        Column(Modifier.fillMaxSize().padding(28.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
            Box(Modifier.size(88.dp).clip(RoundedCornerShape(28.dp)).background(Brush.linearGradient(listOf(Purple, Aqua))), contentAlignment = Alignment.Center) { Text("R", fontSize = 48.sp, fontWeight = FontWeight.Black, color = Color.White) }
            Spacer(Modifier.height(24.dp)); Text("RHA Connect", fontSize = 34.sp, fontWeight = FontWeight.Bold); Text("Talk. Share. Stay close.", color = Muted, fontSize = 16.sp)
            Spacer(Modifier.height(48.dp))
            Button(onClick = onContinue, Modifier.fillMaxWidth().height(56.dp), shape = RoundedCornerShape(18.dp), colors = ButtonDefaults.buttonColors(containerColor = Color.White, contentColor = Ink)) { Text("G  Continue with Google", fontSize = 16.sp, fontWeight = FontWeight.Bold) }
            Spacer(Modifier.height(14.dp)); OutlinedButton(onClick = onContinue, Modifier.fillMaxWidth().height(56.dp), shape = RoundedCornerShape(18.dp)) { Text("Create account with email") }
            Spacer(Modifier.height(22.dp)); Text("Your account is simple, secure and ready in seconds.", color = Muted, fontSize = 12.sp)
        }
    }
}

private enum class Tab { HOME, REELS, CHATS, PROFILE }
private data class Chat(val name: String, val handle: String, val message: String, val time: String, val online: Boolean)
private val chats = listOf(Chat("Ayesha Khan", "@ayeshak", "That reel was amazing!", "09:42", true), Chat("Hamza R.", "@hamza.r", "Voice message · 0:18", "Yesterday", false), Chat("Sana Malik", "@sanam", "Let's catch up soon", "Mon", true))

@Composable private fun HomeShell() {
    var tab by remember { mutableStateOf(Tab.HOME) }; var showSearch by remember { mutableStateOf(false) }; var showCall by remember { mutableStateOf(false) }
    Scaffold(containerColor = Ink, topBar = { TopBar(tab) { showSearch = true } }, bottomBar = {
        NavigationBar(containerColor = Navy, tonalElevation = 0.dp) { NavItem(tab == Tab.HOME, "Home", Icons.Filled.Home) { tab = Tab.HOME }; NavItem(tab == Tab.REELS, "Reels", Icons.Filled.PlayArrow) { tab = Tab.REELS }; NavItem(tab == Tab.CHATS, "Chats", Icons.Filled.ChatBubble) { tab = Tab.CHATS }; NavItem(tab == Tab.PROFILE, "Profile", Icons.Filled.Person) { tab = Tab.PROFILE } }
    }) { pad -> Box(Modifier.padding(pad).fillMaxSize()) { when (tab) { Tab.HOME -> FeedScreen { showCall = true }; Tab.REELS -> ReelsScreen(); Tab.CHATS -> ChatsScreen { showCall = true }; Tab.PROFILE -> ProfileScreen() } } }
    if (showSearch) SearchDialog { showSearch = false }; if (showCall) CallDialog { showCall = false }
}

@Composable private fun TopBar(tab: Tab, onSearch: () -> Unit) { Row(Modifier.fillMaxWidth().padding(horizontal = 20.dp, vertical = 14.dp), verticalAlignment = Alignment.CenterVertically) { Text(if (tab == Tab.REELS) "Discover" else "RHA", fontSize = 26.sp, fontWeight = FontWeight.ExtraBold); Spacer(Modifier.weight(1f)); IconButton(onClick = onSearch) { Icon(Icons.Filled.Search, "Find people") }; IconButton(onClick = {}) { Icon(Icons.Filled.Notifications, "Notifications") } } }
@Composable private fun RowScope.NavItem(selected: Boolean, label: String, icon: androidx.compose.ui.graphics.vector.ImageVector, onClick: () -> Unit) { NavigationBarItem(selected, onClick, icon = { Icon(icon, label) }, label = { Text(label) }, colors = NavigationBarItemDefaults.colors(selectedIconColor = Purple, selectedTextColor = Color.White, indicatorColor = Purple.copy(alpha = .18f), unselectedIconColor = Muted, unselectedTextColor = Muted)) }

@Composable private fun FeedScreen(onCall: () -> Unit) { LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(20.dp), verticalArrangement = Arrangement.spacedBy(18.dp)) { item { StoryRow() }; item { SectionHeader("For you", "See all") }; itemsIndexed(listOf("Weekend energy", "A little sunshine", "Night city walks")) { index, title -> PostCard(title, "@${listOf("ayeshak", "hamza.r", "sanam")[index]}", index, onCall) } } }
@Composable private fun StoryRow() { Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) { Column(Modifier.width(68.dp), horizontalAlignment = Alignment.CenterHorizontally) { Box(Modifier.size(58.dp).clip(CircleShape).background(Purple), contentAlignment = Alignment.Center) { Icon(Icons.Filled.Add, "Add story") }; Text("Your story", fontSize = 11.sp, color = Muted, modifier = Modifier.padding(top = 6.dp)) }; listOf("Ayesha", "Hamza", "Sana", "Maha").forEachIndexed { i, name -> Column(Modifier.width(68.dp), horizontalAlignment = Alignment.CenterHorizontally) { Avatar(name, 54.dp, listOf(Aqua, Purple, Color(0xFFFF8E6C), Color(0xFFF5C451))[i]); Text(name, fontSize = 11.sp, color = Muted, modifier = Modifier.padding(top = 6.dp)) } } } }

@Composable private fun PostCard(title: String, handle: String, index: Int, onCall: () -> Unit) { val colors = listOf(Color(0xFF274B68), Color(0xFF684B83), Color(0xFF3B665D)); Card(Modifier.fillMaxWidth(), shape = RoundedCornerShape(24.dp), colors = CardDefaults.cardColors(containerColor = Card)) { Column { Box(Modifier.fillMaxWidth().height(205.dp).background(Brush.linearGradient(listOf(colors[index], Color(0xFF151A34))))) { Text("REEL  •  0:${18 + index * 7}", Modifier.align(Alignment.TopStart).padding(16.dp), color = Color.White.copy(alpha = .8f), fontSize = 11.sp, fontWeight = FontWeight.Bold); Icon(Icons.Filled.PlayArrow, "Play reel", Modifier.align(Alignment.Center).size(54.dp)); Text(title, Modifier.align(Alignment.BottomStart).padding(16.dp), fontSize = 22.sp, fontWeight = FontWeight.Bold) }; Row(Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) { Avatar(handle.removePrefix("@"), 36.dp, Purple); Spacer(Modifier.width(10.dp)); Column(Modifier.weight(1f)) { Text(handle, fontWeight = FontWeight.SemiBold); Text("2h ago  ·  Public", color = Muted, fontSize = 12.sp) }; IconButton(onClick = {}) { Icon(Icons.Filled.FavoriteBorder, "Like") }; IconButton(onClick = onCall) { Icon(Icons.Filled.Share, "Share") } } } } }

@Composable private fun ReelsScreen() { Box(Modifier.fillMaxSize().background(Color.Black)) { Column(Modifier.fillMaxSize(), verticalArrangement = Arrangement.Bottom) { Box(Modifier.fillMaxWidth().weight(1f).background(Brush.verticalGradient(listOf(Color(0xFF332158), Color(0xFF081B30))))) { Icon(Icons.Filled.PlayArrow, "Play", Modifier.align(Alignment.Center).size(72.dp), tint = Color.White.copy(alpha = .9f)) }; Column(Modifier.padding(20.dp)) { Text("A calm mind is a powerful thing.", fontSize = 18.sp, fontWeight = FontWeight.Bold); Text("@ayeshak  ·  Original audio", color = Muted, modifier = Modifier.padding(top = 8.dp)) }; Row(Modifier.fillMaxWidth().padding(12.dp), horizontalArrangement = Arrangement.SpaceEvenly) { IconButton(onClick = {}) { Icon(Icons.Filled.FavoriteBorder, "Like") }; IconButton(onClick = {}) { Icon(Icons.Filled.Comment, "Comment") }; IconButton(onClick = {}) { Icon(Icons.Filled.Share, "Share") } } } } }

@Composable private fun ChatsScreen(onCall: () -> Unit) { var selected by remember { mutableStateOf<Chat?>(null) }; if (selected == null) { LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(20.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) { item { Text("Messages", fontSize = 30.sp, fontWeight = FontWeight.Bold); Text("Private, fast and human.", color = Muted, modifier = Modifier.padding(top = 4.dp, bottom = 18.dp)) }; item { Button(onClick = {}, Modifier.fillMaxWidth().height(52.dp), shape = RoundedCornerShape(16.dp)) { Icon(Icons.Filled.Add, null); Spacer(Modifier.width(8.dp)); Text("Start a new chat") } }; items(chats) { chat -> ChatRow(chat) { selected = chat } } } } else ChatDetail(selected!!, onBack = { selected = null }, onCall = onCall) }
@Composable private fun ChatRow(chat: Chat, onClick: () -> Unit) { Row(Modifier.fillMaxWidth().clip(RoundedCornerShape(18.dp)).clickable(onClick = onClick).padding(12.dp), verticalAlignment = Alignment.CenterVertically) { Box { Avatar(chat.name, 52.dp, Purple); if (chat.online) Box(Modifier.size(13.dp).clip(CircleShape).background(Aqua).align(Alignment.BottomEnd)) }; Spacer(Modifier.width(14.dp)); Column(Modifier.weight(1f)) { Text(chat.name, fontWeight = FontWeight.Bold); Text(chat.message, color = Muted, maxLines = 1) }; Text(chat.time, color = Muted, fontSize = 11.sp) } }

@Composable private fun ChatDetail(chat: Chat, onBack: () -> Unit, onCall: () -> Unit) { var text by remember { mutableStateOf("") }; var recording by remember { mutableStateOf(false) }; Column(Modifier.fillMaxSize()) { Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) { IconButton(onClick = onBack) { Icon(Icons.Filled.ArrowBack, "Back") }; Avatar(chat.name, 40.dp, Purple); Spacer(Modifier.width(10.dp)); Column(Modifier.weight(1f)) { Text(chat.name, fontWeight = FontWeight.Bold); Text(if (chat.online) "Online" else "Last seen recently", color = if (chat.online) Aqua else Muted, fontSize = 12.sp) }; IconButton(onClick = onCall) { Icon(Icons.Filled.Call, "Audio call") }; IconButton(onClick = onCall) { Icon(Icons.Filled.Videocam, "Video call") } }; Divider(color = Color.White.copy(alpha = .08f)); LazyColumn(Modifier.weight(1f), contentPadding = PaddingValues(20.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) { item { Text("Today", modifier = Modifier.fillMaxWidth(), color = Muted, fontSize = 12.sp); MessageBubble("Hey! Welcome to RHA Connect.", false); MessageBubble("Thanks — this feels really smooth.", true); MessageBubble("Send a voice note or start a call anytime.", false) } }; Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) { IconButton(onClick = { recording = !recording }) { Icon(if (recording) Icons.Filled.Stop else Icons.Filled.Mic, "Voice message", tint = if (recording) Color.Red else Aqua) }; OutlinedTextField(text, { text = it }, Modifier.weight(1f), placeholder = { Text("Write a message…") }, shape = RoundedCornerShape(20.dp), singleLine = true, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Text)); IconButton(onClick = { text = "" }) { Icon(Icons.Filled.Send, "Send", tint = Purple) } }; AnimatedVisibility(recording) { Text("Recording voice message… tap the mic to finish", Modifier.fillMaxWidth().padding(bottom = 12.dp), color = Color.Red, fontSize = 12.sp, textAlign = androidx.compose.ui.text.style.TextAlign.Center) } } }
@Composable private fun MessageBubble(text: String, mine: Boolean) { Row(Modifier.fillMaxWidth(), horizontalArrangement = if (mine) Arrangement.End else Arrangement.Start) { Surface(color = if (mine) Purple else Card, shape = RoundedCornerShape(18.dp, 18.dp, if (mine) 4.dp else 18.dp, if (mine) 18.dp else 4.dp)) { Text(text, Modifier.padding(14.dp)) } } }

@Composable private fun ProfileScreen() { val context = LocalContext.current; val launcher = rememberLauncherForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { Toast.makeText(context, "Permissions updated", Toast.LENGTH_SHORT).show() }; Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp)) { Row(verticalAlignment = Alignment.CenterVertically) { Avatar("Raha", 84.dp, Purple); Spacer(Modifier.width(18.dp)); Column { Text("Raha Haider", fontSize = 23.sp, fontWeight = FontWeight.Bold); Text("@raha", color = Aqua); Text("Building meaningful conversations.", color = Muted, modifier = Modifier.padding(top = 6.dp)) } }; Spacer(Modifier.height(24.dp)); Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) { Stat("128", "Following"); Stat("2.4K", "Followers"); Stat("48", "Reels") }; Spacer(Modifier.height(24.dp)); Button(onClick = { launcher.launch(arrayOf(Manifest.permission.RECORD_AUDIO, Manifest.permission.CAMERA, Manifest.permission.READ_EXTERNAL_STORAGE)) }, Modifier.fillMaxWidth().height(52.dp), shape = RoundedCornerShape(16.dp)) { Icon(Icons.Filled.Security, null); Spacer(Modifier.width(8.dp)); Text("Permissions & privacy") }; Spacer(Modifier.height(14.dp)); OutlinedButton(onClick = {}, Modifier.fillMaxWidth().height(52.dp), shape = RoundedCornerShape(16.dp)) { Icon(Icons.Filled.Settings, null); Spacer(Modifier.width(8.dp)); Text("Account settings") }; Spacer(Modifier.height(24.dp)); Text("Cloud media", fontSize = 18.sp, fontWeight = FontWeight.Bold); Text("Your photos, videos and voice notes are ready for secure Cloudinary delivery.", color = Muted, modifier = Modifier.padding(top = 6.dp)); Spacer(Modifier.height(16.dp)); MediaTile() } }
@Composable private fun RowScope.Stat(value: String, label: String) { Column(Modifier.weight(1f).clip(RoundedCornerShape(16.dp)).background(Card).padding(14.dp), horizontalAlignment = Alignment.CenterHorizontally) { Text(value, fontWeight = FontWeight.Bold, fontSize = 20.sp); Text(label, color = Muted, fontSize = 11.sp) } }
@Composable private fun MediaTile() { Box(Modifier.fillMaxWidth().height(130.dp).clip(RoundedCornerShape(20.dp)).background(Brush.horizontalGradient(listOf(Color(0xFF284D65), Color(0xFF5D397A))))) { Column(Modifier.align(Alignment.Center), horizontalAlignment = Alignment.CenterHorizontally) { Icon(Icons.Filled.CloudUpload, null, Modifier.size(30.dp)); Text("Upload media", Modifier.padding(top = 8.dp), fontWeight = FontWeight.Bold); Text("Cloudinary secured", color = Color.White.copy(alpha = .7f), fontSize = 12.sp) } } }
@Composable private fun SearchDialog(onClose: () -> Unit) { var query by remember { mutableStateOf("") }; AlertDialog(onDismissRequest = onClose, confirmButton = { Button(onClick = onClose) { Text("Done") } }, title = { Text("Find someone") }, text = { Column { OutlinedTextField(query, { query = it }, Modifier.fillMaxWidth(), label = { Text("Username") }, placeholder = { Text("@username") }); if (query.isNotBlank()) Text("Matching profiles for $query", color = Aqua, modifier = Modifier.padding(top = 16.dp)) } }) }
@Composable private fun CallDialog(onClose: () -> Unit) { AlertDialog(onDismissRequest = onClose, confirmButton = { Button(onClick = onClose) { Text("Close") } }, icon = { Icon(Icons.Filled.Videocam, null, tint = Purple) }, title = { Text("Call ready") }, text = { Text("Audio and video calling is prepared for your realtime backend. Camera and microphone permissions are available in Profile → Permissions & privacy.") }) }
@Composable private fun Avatar(name: String, size: Dp, color: Color) { Box(Modifier.size(size).clip(CircleShape).background(color), contentAlignment = Alignment.Center) { Text(name.take(1).uppercase(), color = Color.White, fontWeight = FontWeight.Bold, fontSize = (size.value / 2.8f).sp) } }
@Composable private fun SectionHeader(title: String, action: String) { Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) { Text(title, fontSize = 21.sp, fontWeight = FontWeight.Bold); Spacer(Modifier.weight(1f)); Text(action, color = Aqua, fontSize = 13.sp) } }
