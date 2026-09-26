from typing import Dict, Any, Tuple

class LanguageRouter:
    def __init__(self, config: dict):
        self.config = config

    def detect_and_normalize(self, text: str) -> Tuple[str, float, str]:
        """
        Takes raw recognized text and returns:
        - language (str) e.g., 'urdu', 'english', 'roman_urdu', 'mixed'
        - confidence (float)
        - normalized_text (str)
        """
        # Placeholder logic
        text_lower = text.lower().strip()
        
        # Simple heuristic
        if "kholo" in text_lower or "karo" in text_lower:
            return "roman_urdu", 0.9, text_lower
        elif any(c in "ابپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنںوؤہہیئے" for c in text):
            return "urdu", 0.95, text_lower
        else:
            return "english", 0.9, text_lower
