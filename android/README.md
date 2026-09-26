# RHA Android Native Integration (Phases 16 & 20)

This directory contains the structural skeleton for the native Kotlin Android application.

## Architecture
Rather than running purely in Termux, the native app wraps the Python engine using **Chaquopy** (a Python SDK for Android).

1. `RhaVoiceService.kt` runs as a Android Foreground Service with a persistent notification.
2. It holds a `WAKE_LOCK` and keeps the microphone active via `AudioRecord`.
3. It passes byte arrays directly to the Python `RHAEngine` running in the Chaquopy JVM bridge.

## Production Packaging (APK Build)
To build the final APK (Phase 20):
1. Open this `android/` directory in **Android Studio**.
2. Sync Gradle (Chaquopy plugin will download necessary Python environments for ARM64).
3. Place `config/`, `models/`, and `engine/` inside the `src/main/python/` assets directory (automated via gradle copy script in a full build).
4. Build -> Build Bundle(s) / APK(s) -> Build APK.

*Note: Model files (.gguf, .onnx) should be downloaded at runtime to keep the APK size under the Play Store limits.*
