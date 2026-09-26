# RHA Local Voice Engine: Complete Termux Setup & Testing Guide

This guide provides step-by-step instructions for deploying and running the **100% Offline RHA Voice Engine** directly on your Android phone using Termux. 

By following this guide, your phone will act as a fully autonomous AI voice assistant without needing the cloud.

---

## 🛑 Prerequisites: Essential Android Apps

Before touching the terminal, you must install the correct Android apps. **Do NOT use the Google Play Store versions of Termux**, as they are outdated and broken.

1. Download **F-Droid** (an open-source app store) from [f-droid.org](https://f-droid.org/).
2. Open F-Droid and search for **Termux**. Install it.
3. Search for **Termux:API** in F-Droid. Install it.
   - *Why?* The Termux:API app bridges the terminal to your Android system, allowing the RHA engine to actually execute commands like opening YouTube, checking your battery, and controlling your volume.

---

## 🛠️ Step 1: Initial Termux Configuration

Open the **Termux** app on your phone. We need to prepare your storage and ensure core Linux packages are up to date.

```bash
# 1. Grant storage permissions (a popup will appear on your phone, click "Allow")
termux-setup-storage

# 2. Update all existing packages (hit 'y' or enter if it asks you during the process)
pkg update -y && pkg upgrade -y

# 3. Install git to download the repository
pkg install git -y
```

---

## 📥 Step 2: Download the RHA Engine

Clone your completed repository from GitHub to your phone:

```bash
# Clone the repository
git clone https://github.com/rajahaider50/rha-local-voice-engine.git

# Navigate into the project folder
cd rha-local-voice-engine
```

---

## ⚙️ Step 3: Run the Automated Setup

We have provided a script that installs Python, audio dependencies, Termux API packages, and sets up an isolated virtual environment.

```bash
# Run the automated setup script
bash scripts/setup_termux.sh

# Activate the Python virtual environment
source venv/bin/activate
```
*Note: This might take a few minutes depending on your phone's processor.*

---

## 🧠 Step 4: Download the Offline AI Models

Because the engine is 100% offline, you need to download the AI "brains" to your phone's storage. We wrote an automated script for this.

```bash
# Downloads Whisper.cpp (STT) and Qwen (LLM) models
python scripts/download_models.py
```
*(Ensure you are on Wi-Fi. This will download ~1.3GB of highly optimized AI models directly to your `models/` directory).*

---

## 🚀 Step 5: Start the Master Voice Assistant

Everything is now ready. You can start the master pipeline which controls the Wake Word, the Microphone, the VAD, the Intent Router, and the LLM.

```bash
# Ensure you are still in the venv
source venv/bin/activate

# Start the full engine
python engine/core/pipeline.py
```

### How to use it:
1. The terminal will print `Waiting for wake word...`
2. Say **"Hey Jarvis"** loudly into your phone.
3. The engine will beep/print `WAKE WORD DETECTED!` and switch to **Listening Mode**.
4. Say a command in Roman Urdu (e.g., *"YouTube kholo"*) or ask a question in English (*"What is a black hole?"*).
5. The engine will stop listening when you pause, process your speech offline, and instantly execute the action or reply with the AI!

---

## 🔄 Optional: Running as a Background Daemon

If you want the assistant to listen for the wake word even while your phone screen is off, you can run it as a background service:

```bash
# Starts the engine in the background and acquires a CPU wake-lock
./scripts/start_termux_service.sh
```

To stop it and save battery:
```bash
./scripts/stop_termux_service.sh
```

---

## 🐞 Troubleshooting

**Error: "termux-open: command not found" or "battery status fails"**
- Ensure you installed the `Termux:API` app from F-Droid.
- Run `pkg install termux-api` manually in Termux.

**Error: "ALSA lib pcm.c... Unknown PCM" or PyAudio crashes**
- Termux handles audio differently than a desktop Linux. Ensure you accepted microphone permissions. 
- You may need to start pulseaudio: `pulseaudio --start`

**Cannot install `llama-cpp-python` or `whisper-cpp-python` during pip install?**
- Mobile compilation requires specific CMake flags. Ensure you run:
  `CMAKE_ARGS="-DGGML_TERMUX=ON" pip install llama-cpp-python whisper-cpp-python`
