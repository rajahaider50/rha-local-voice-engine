import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from engine.intent.router import IntentRouter
from engine.language.router import LanguageRouter

def test_intent_routing():
    lang_router = LanguageRouter()
    intent_router = IntentRouter()
    
    # Test Roman Urdu App Open
    lang, conf, norm = lang_router.detect_and_normalize("youtube kholo")
    assert lang == "roman_urdu"
    
    intent, params, conf = intent_router.route_intent(norm, lang)
    assert intent == "OPEN_APP"
    assert params.get("app") == "youtube"
    
    # Test English Conversational Fallback
    lang, conf, norm = lang_router.detect_and_normalize("what is a black hole")
    assert lang == "english"
    
    intent, params, conf = intent_router.route_intent(norm, lang)
    assert intent == "CONVERSATIONAL"

if __name__ == "__main__":
    pytest.main([__file__])
