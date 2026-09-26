import yaml
from typing import Tuple

class LanguageRouter:
    def __init__(self, config_path: str = "config/languages.yaml"):
        """
        Initializes the Language Router.
        Loads normalization rules for Roman Urdu.
        """
        self.config_path = config_path
        self.rules = self._load_rules()

    def _load_rules(self) -> dict:
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get("normalization_rules", {}).get("roman_urdu", [])
        except Exception as e:
            print(f"[LanguageRouter] Error loading rules: {e}")
            return []

    def detect_and_normalize(self, text: str) -> Tuple[str, float, str]:
        """
        Takes raw recognized text and returns:
        - language (str) e.g., 'urdu', 'english', 'roman_urdu', 'mixed'
        - confidence (float)
        - normalized_text (str)
        """
        if not text:
            return "unknown", 0.0, ""
            
        text_lower = text.lower().strip()
        
        # 1. Detect pure Urdu script
        # Check if text contains Arabic/Urdu characters
        urdu_chars = "ابپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنںوؤہہیئے"
        urdu_count = sum(1 for c in text if c in urdu_chars)
        
        if urdu_count > 0:
            if urdu_count > len(text) * 0.5:
                return "urdu", 0.95, text_lower
            else:
                return "mixed_urdu_english", 0.8, text_lower

        # 2. Detect Roman Urdu vs English
        # Very simple heuristic: check for common Roman Urdu verbs
        roman_urdu_keywords = ["kholo", "karo", "chalao", "batao", "hai", "mera", "mujhe", "kya"]
        roman_count = sum(1 for word in text_lower.split() if word in roman_urdu_keywords)
        
        normalized_text = text_lower
        
        if roman_count > 0:
            # Apply normalization rules
            for rule in self.rules:
                pattern = rule.get("pattern", "")
                replacement = rule.get("replacement", "")
                if pattern and replacement:
                    normalized_text = normalized_text.replace(pattern, replacement)
            return "roman_urdu", 0.85, normalized_text
            
        # 3. Default to English
        return "english", 0.9, text_lower
