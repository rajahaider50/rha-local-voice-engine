import yaml
from typing import Dict, Any, Tuple

class IntentRouter:
    def __init__(self, config_path: str = "config/commands.yaml"):
        """
        Fast, deterministic intent matching before hitting the LLM.
        """
        self.config_path = config_path
        self.intents = self._load_intents()

    def _load_intents(self) -> dict:
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get("intents", {})
        except Exception as e:
            print(f"[IntentRouter] Error loading intents: {e}")
            return {}

    def route_intent(self, normalized_text: str, language: str) -> Tuple[str, Dict[str, Any], float]:
        """
        Matches text against regex/keywords.
        Returns: intent_name, parameters, confidence
        """
        # Map our detected languages to the yaml keys
        lang_key = "english"
        if language in ["urdu", "mixed_urdu_english"]:
            lang_key = "urdu"
        elif language == "roman_urdu":
            lang_key = "roman_urdu"

        for intent_name, data in self.intents.items():
            keywords = data.get("keywords", {}).get(lang_key, [])
            # Also check english keywords as fallback for mixed language
            if lang_key != "english":
                keywords.extend(data.get("keywords", {}).get("english", []))
                
            for kw in keywords:
                if kw in normalized_text:
                    params = {}
                    if intent_name == "OPEN_APP":
                        app_name = normalized_text.replace(kw, "").strip()
                        if app_name:
                            params["app"] = app_name
                    elif intent_name == "WEB_SEARCH":
                        query = normalized_text.replace(kw, "").strip()
                        if query:
                            params["query"] = query
                            
                    return intent_name, params, 0.95
        
        # If no deterministic intent is found, route to CONVERSATIONAL for the LLM
        return "CONVERSATIONAL", {"text": normalized_text}, 1.0
