#!/usr/bin/env python3
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from engine.audio.capture import AudioCapture
from engine.vad.detector import VoiceActivityDetector

def main():
    print("=======================================")
    print(" RHA VAD Test (Phase 3)                ")
    print("=======================================")
    
    # 512 frames @ 16kHz = 32ms chunks (standard for VAD)
    capture = AudioCapture(sample_rate=16000, chunk_size=512, channels=1)
    vad = VoiceActivityDetector(sample_rate=16000, threshold=0.5)
    
    print("Listening... (Press Ctrl+C to stop)")
    print("Say something to test the Voice Activity Detector.")
    
    try:
        for chunk in capture.start_stream():
            if vad.is_speech(chunk):
                print("🗣️  SPEECH DETECTED")
            else:
                # Print a dot for silence to show it's working
                sys.stdout.write('.')
                sys.stdout.flush()
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    finally:
        capture.terminate()

if __name__ == "__main__":
    main()
