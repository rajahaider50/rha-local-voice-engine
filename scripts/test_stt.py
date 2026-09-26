#!/usr/bin/env python3
import sys
import os
import wave
import time

# Add the project root to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from engine.audio.capture import AudioCapture
from engine.vad.detector import VoiceActivityDetector
from engine.stt.whisper_engine import WhisperEngine

def main():
    print("=======================================")
    print(" RHA Speech-to-Text Test (Phase 5)     ")
    print("=======================================")
    
    print("\n[Init] Initializing AI models. This may take a moment and download ~140MB of data on first run...")
    
    try:
        stt = WhisperEngine()
        vad = VoiceActivityDetector()
        capture = AudioCapture(sample_rate=16000, chunk_size=1024, channels=1)
    except Exception as e:
        print(f"Failed to initialize components: {e}")
        return

    print("\nSystem Ready!")
    print("Speak clearly into your microphone in English or Urdu.")
    print("Press Ctrl+C to stop.\n")
    
    # We will buffer audio while speaking, and process it when silence is detected
    audio_buffer = []
    is_speaking_state = False
    silence_frames = 0
    SILENCE_THRESHOLD = 20 # Number of chunks of silence before considering speech ended
    
    try:
        for chunk in capture.start_stream():
            is_speech = vad.is_speech(chunk)
            
            if is_speech:
                if not is_speaking_state:
                    print("\n[Speech Detected] Recording...", end="", flush=True)
                    is_speaking_state = True
                audio_buffer.append(chunk)
                silence_frames = 0
            elif is_speaking_state:
                silence_frames += 1
                audio_buffer.append(chunk) # Add trailing silence
                
                if silence_frames > SILENCE_THRESHOLD:
                    print("\n[Processing] Transcribing audio...")
                    is_speaking_state = False
                    
                    # Combine all recorded chunks
                    full_audio = b"".join(audio_buffer)
                    
                    # Transcribe
                    start_time = time.time()
                    text = stt.transcribe_audio(full_audio)
                    end_time = time.time()
                    
                    latency = round(end_time - start_time, 2)
                    
                    print(f"\n🗣️  User: \"{text}\"")
                    print(f"⏱️  Latency: {latency}s")
                    print("-" * 40)
                    
                    # Clear buffer for next speech
                    audio_buffer = []
                    print("\nListening...")
            
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    finally:
        capture.terminate()

if __name__ == "__main__":
    main()
