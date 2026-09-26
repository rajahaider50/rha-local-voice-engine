# RHA LOCAL VOICE ENGINE

Professional 100% Local, Free & Offline AI Voice Assistant.

## Overview

RHA Local Voice Engine is a fast, clean, lightweight, professional, privacy-first voice assistant designed to understand and respond to Urdu, English, Roman Urdu, and mixed Urdu-English speech completely locally without paid APIs or cloud AI services.

The architecture is modular, lightweight, replaceable, testable, and optimized for Android/mobile hardware.

## Core Features

- **100% Offline & Local**: No OpenAI, Gemini, Claude, or ElevenLabs APIs.
- **Multilingual**: Supports Urdu, English, Roman Urdu, and mixed language input.
- **Streaming Pipeline**: Low latency STT, LLM generation, and TTS.
- **Fast Intent Engine**: Deterministic routing for common commands to avoid unnecessary LLM overhead.
- **Wake Word**: Local wake word detection (openWakeWord).
- **VAD**: Voice Activity Detection to minimize resource usage.
- **Privacy-First**: No data uploaded without explicit consent. SQLite local memory.

## Architecture

The system is modular:
- `engine/core/`: Event loop, pipeline management.
- `engine/audio/`: Capture, resampling, VAD.
- `engine/wakeword/`: Wake word detection.
- `engine/stt/`: Speech-to-Text (whisper.cpp).
- `engine/language/`: Language detection and normalization.
- `engine/intent/`: Fast intent routing.
- `engine/llm/`: Local LLM (llama.cpp).
- `engine/tts/`: Text-to-Speech (English & Urdu).
- `engine/memory/`: Local SQLite memory.
- `engine/tools/`: Android/System commands.

## Getting Started

See `scripts/setup_termux.sh` for Termux installation or `scripts/install.sh` for standard Linux setup.
