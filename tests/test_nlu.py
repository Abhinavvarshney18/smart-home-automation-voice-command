from app.nlu import NLUEvaluator

def test_nlu_predict_basic():
    n = NLUEvaluator()
    res = n.predict("please turn on the lights")
    assert "intent" in res and res["intent"].startswith("light")
