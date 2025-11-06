from app.intent_classifier import IntentClassifier

def test_predict_light_on():
    ic = IntentClassifier()
    r = ic.predict("please turn on the lights in the living room")
    assert "light_on" in r["scores"] or r["intent"] == "light_on"
