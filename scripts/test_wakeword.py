#!/usr/bin/env python3
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from engine.audio.capture import AudioCapture
from engine.wakeword.detector import WakeWordDetector

def main():
    print("=======================================")
    print(" RHA Wake Word Test (Phase 4)          ")
    print("=======================================")
    
    # openWakeWord expects 1280 frame chunks (80ms at 16kHz) for optimal performance
    capture = AudioCapture(sample_rate=16000, chunk_size=1280, channels=1)
    
    # We use the default 'hey_jarvis' for this test since we haven't trained 'Hey RHA' yet
    detector = WakeWordDetector(threshold=0.5)
    
    print("\nListening... (Press Ctrl+C to stop)")
    print("Say 'Hey Jarvis' to trigger the wake word.")
    
    try:
        for chunk in capture.start_stream():
            if detector.process_chunk(chunk):
                print("\n🔔 WAKE WORD DETECTED! ('Hey Jarvis')")
                print("In a full system, we would now begin Speech-to-Text recording...\n")
                print("Resuming listening...")
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    finally:
        capture.terminate()

if __name__ == "__main__":
    main()
