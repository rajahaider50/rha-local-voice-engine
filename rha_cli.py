#!/usr/bin/env python3
import sys
import json
import urllib.request
import urllib.error

API_URL = "http://localhost:8000/api/v1/test_intent"

def send_command(text: str):
    data = json.dumps({"text": text, "language": "auto"}).encode("utf-8")
    req = urllib.request.Request(
        API_URL, 
        data=data, 
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"\n[RHA Engine]")
            print(f"Intent:   {result.get('intent')}")
            print(f"Language: {result.get('language_detected')}")
            print(f"Response: {result.get('response')}\n")
    except urllib.error.URLError as e:
        print(f"Error connecting to RHA local service: {e}")
        print("Make sure the background service is running (./scripts/start_termux_service.sh)")

def main():
    print("=======================================")
    print(" RHA LOCAL VOICE ENGINE - TERMINAL CLI ")
    print("=======================================")
    print("Type your commands below (Urdu, English, Roman Urdu).")
    print("Type 'exit' or 'quit' to close.")
    
    while True:
        try:
            cmd = input("\nYou: ")
            if cmd.lower() in ["exit", "quit"]:
                break
            if cmd.strip():
                send_command(cmd)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
