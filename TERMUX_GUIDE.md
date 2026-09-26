# RHA Local Voice Engine: Termux Setup & Testing Guide

This guide provides step-by-step instructions for deploying and testing the **RHA Local Voice Engine** directly on your Android phone using Termux. 

By following this guide, you will have a local AI daemon running in the background of your phone that can execute Android commands offline.

---

## 🛑 Prerequisites

Before touching the terminal, you must install the correct Android apps. **Do NOT use the Google Play Store versions of Termux**, as they are outdated and broken.

1. Download **F-Droid** (an open-source app store) from [f-droid.org](https://f-droid.org/).
2. Open F-Droid and search for **Termux**. Install it.
3. Search for **Termux:API** in F-Droid. Install it.
   - *Why?* The Termux:API app bridges the terminal to your Android system, allowing the RHA engine to open apps, check battery, change volume, and toggle the flashlight.

---

## 🛠️ Step 1: Initial Termux Configuration

Open the **Termux** app on your phone and run the following commands to prepare your storage and ensure everything is up to date:

```bash
# 1. Grant storage permissions to Termux (a popup will appear on your phone, click "Allow")
termux-setup-storage

# 2. Update all existing packages
pkg update -y && pkg upgrade -y

# 3. Install git to download the repository
pkg install git -y
```

---

## 📥 Step 2: Download the Engine

Clone the repository from GitHub to your phone:

```bash
# Clone your repository
git clone https://github.com/rajahaider50/rha-local-voice-engine.git

# Navigate into the project folder
cd rha-local-voice-engine
```

---

## ⚙️ Step 3: Run the Setup Script

We have provided an automated script that installs Python, audio dependencies, Termux API packages, and sets up a virtual environment.

```bash
# Run the automated setup script
bash scripts/setup_termux.sh
```

*Note: This might take a few minutes depending on your phone's processor and internet connection.*

---

## 🚀 Step 4: Start the RHA Background Service

The RHA Engine runs as a lightweight, local API server (daemon). We've provided scripts to manage it so Android doesn't kill it when you turn off your screen.

To start the engine:

```bash
# Starts the engine and acquires a CPU wake-lock
./scripts/start_termux_service.sh
```

**How to know it's working?**
It will output: `RHA Service started in the background (PID: XXXX)`.
All logs are saved to `rha_service.log`. You can view them anytime by running:
`cat rha_service.log`

---

## 🧪 Step 5: Testing the Intent Engine (CLI)

Because the microphone and AI models (Whisper/Qwen) are scheduled for later phases, we have built a **Terminal CLI** so you can immediately test the intent recognition and language routing logic.

With the background service running, launch the CLI:

```bash
./rha_cli.py
```

### Example Test Cases to Try:

1. **Test Roman Urdu Application Launching:**
   - Type: `youtube kholo`
   - *Expected Intent: OPEN_APP*
   - *Expected Language: roman_urdu*

2. **Test English Conversational Fallback:**
   - Type: `explain black holes in simple words`
   - *Expected Intent: CONVERSATIONAL*
   - *Expected Language: english*

3. **Test Native System Commands:**
   - Type: `open calculator`
   - *Expected Intent: OPEN_APP*

Type `exit` to close the CLI when you are done.

---

## 🛑 Step 6: Stopping the Service

When you are done testing, you must stop the background service to release the CPU wake-lock and save your phone's battery.

```bash
./scripts/stop_termux_service.sh
```

---

## 🐞 Troubleshooting

**Error: "termux-open: command not found" or "battery status fails"**
- Ensure you installed the `Termux:API` app from F-Droid.
- Ensure you ran `pkg install termux-api` (this is handled automatically by `setup_termux.sh`).

**Error: "Error connecting to RHA local service: Connection refused"**
- The background daemon is not running. Run `./scripts/start_termux_service.sh` again and check `cat rha_service.log` for Python errors.

**Cannot install `llama-cpp-python` or `whisper-cpp-python`?**
- Mobile compilation requires specific flags. When we reach the AI deployment phase, you will use:
  `CMAKE_ARGS="-DGGML_TERMUX=ON" pip install llama-cpp-python`
