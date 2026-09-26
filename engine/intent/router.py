from typing import Dict, Any, Tuple

class IntentRouter:
    def __init__(self, config: dict):
        self.config = config

    def route_intent(self, normalized_text: str) -> Tuple[str, Dict[str, Any], float]:
        """
        Takes normalized text and returns:
        - intent (str)
        - parameters (dict)
        - confidence (float)
        """
        # Placeholder for regex/keyword matching logic
        # Example: if "kholo" in text -> intent: OPEN_APP
        
        # Fallback
        return "UNKNOWN_INTENT", {}, 0.0
