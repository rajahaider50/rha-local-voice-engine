#!/usr/bin/env python3
import sys
import os
import wave

# Add the project root to the python path so we can import engine
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from engine.audio.capture import AudioCapture

def main():
    try:
        import pyaudio
    except ImportError:
        print("PyAudio is not installed; install a Termux-compatible audio backend first.")
        return 1
    print("=======================================")
    print(" RHA Audio Capture Test (Phase 2)      ")
    print("=======================================")
    
    output_filename = "test_recording.wav"
    capture = AudioCapture(sample_rate=16000, chunk_size=1024, channels=1)
    
    # We will record for 5 seconds to test
    CHUNKS_TO_RECORD = int((16000 / 1024) * 5)  # 5 seconds
    
    frames = []
    
    print("Recording will start immediately and last for 5 seconds...")
    print("Speak into your microphone!")
    
    try:
        count = 0
        for chunk in capture.start_stream():
            frames.append(chunk)
            count += 1
            if count % 10 == 0:
                print(f"Recording... {count}/{CHUNKS_TO_RECORD} chunks")
                
            if count >= CHUNKS_TO_RECORD:
                break
    except KeyboardInterrupt:
        print("\nRecording interrupted by user.")
    finally:
        capture.terminate()
        
    print(f"\nRecording complete. Saving to {output_filename}...")
    
    # Save the recorded data as a WAV file
    pa = pyaudio.PyAudio()
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))
    pa.terminate()
    print(f"Success! You can listen to {output_filename} to verify audio quality.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
