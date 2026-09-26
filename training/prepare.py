#!/usr/bin/env python3
import json
import os

def prepare_dataset(input_file: str, output_file: str):
    """
    Phase 19: Fine-Tuning Preparation.
    Converts raw intent logs into a JSONL format suitable for LoRA/QLoRA 
    fine-tuning of the Qwen model for better Roman Urdu intent classification.
    """
    print(f"Preparing dataset for fine-tuning...")
    
    # Mock data generation for demonstration
    mock_data = [
        {"text": "youtube kholo", "language": "roman_urdu", "intent": "OPEN_APP", "app": "youtube"},
        {"text": "volume kam karo", "language": "roman_urdu", "intent": "SET_VOLUME"},
        {"text": "what is black hole", "language": "english", "intent": "CONVERSATIONAL"}
    ]
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in mock_data:
            # Format as conversation for instruction tuning
            instruction = f"Analyze this text in {item['language']}: '{item['text']}'"
            response = json.dumps({"intent": item['intent'], "parameters": {k:v for k,v in item.items() if k not in ['text', 'language', 'intent']}})
            
            line = {
                "messages": [
                    {"role": "system", "content": "You are RHA Intent Router."},
                    {"role": "user", "content": instruction},
                    {"role": "assistant", "content": response}
                ]
            }
            f.write(json.dumps(line) + "\n")
            
    print(f"Dataset saved to {output_file}. Ready for QLoRA fine-tuning.")

if __name__ == "__main__":
    prepare_dataset("raw_logs.txt", "training/dataset.jsonl")
