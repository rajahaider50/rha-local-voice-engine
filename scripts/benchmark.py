#!/usr/bin/env python3
import time
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from engine.core.hardware import HardwareProfiler
from engine.stt.whisper_engine import WhisperEngine

def main():
    print("=======================================")
    print(" RHA Real-Device Benchmark (Phase 18)  ")
    print("=======================================")
    
    device_info = HardwareProfiler.get_device_info()
    profile = HardwareProfiler.get_profile()
    
    print(f"Detected Hardware: {device_info['os']} - {device_info['ram_total_gb']}GB RAM")
    print(f"Recommended Profile: {profile}")
    
    # Save device info
    os.makedirs("benchmarks", exist_ok=True)
    with open("benchmarks/device_info.json", "w") as f:
        json.dump(device_info, f, indent=4)
        
    print("\n[Benchmarking] Loading models... (This may take a moment)")
    
    results = {}
    
    # 1. STT Load Time
    start = time.time()
    stt = WhisperEngine()
    results['stt_load_time'] = round(time.time() - start, 2)
    
    # 2. STT Inference Time (Mock empty audio chunk of 1 second)
    empty_audio = b'\x00' * 32000 # 1 second of 16kHz 16-bit mono
    start = time.time()
    stt.transcribe_audio(empty_audio)
    results['stt_inference_1s_audio'] = round(time.time() - start, 2)
    
    # (LLM and TTS benchmarks would follow similarly)
    
    with open("benchmarks/benchmark.json", "w") as f:
        json.dump(results, f, indent=4)
        
    with open("benchmarks/report.md", "w") as f:
        f.write("# RHA Benchmark Report\n\n")
        f.write(f"**Profile:** {profile}\n\n")
        f.write("### Hardware\n```json\n" + json.dumps(device_info, indent=2) + "\n```\n\n")
        f.write("### Latency Results (seconds)\n```json\n" + json.dumps(results, indent=2) + "\n```\n")

    print(f"\nBenchmarks completed! Saved to benchmarks/report.md")

if __name__ == "__main__":
    main()
