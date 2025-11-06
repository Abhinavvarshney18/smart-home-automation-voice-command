from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

class IntentClassifier:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.model = LogisticRegression(max_iter=200)
        self._train_default()

    def _train_default(self):
        X = [
            "turn on the light", "switch on living room light", "lights on",
            "turn off the light", "switch off light", "lights off",
            "lock the door", "unlock the door", "open the door", "close the door",
            "turn on fan", "turn off fan"
        ]
        y = [
            "light_on", "light_on", "light_on",
            "light_off", "light_off", "light_off",
            "lock", "unlock", "unlock", "lock",
            "fan_on", "fan_off"
        ]
        Xv = self.vectorizer.fit_transform(X)
        self.model.fit(Xv, y)

    def predict(self, text: str):
        Xv = self.vectorizer.transform([text or ""])
        intent = self.model.predict(Xv)[0]
        probs = self.model.predict_proba(Xv)[0]
        scores = dict(zip(self.model.classes_, probs))
        return {"intent": intent, "scores": scores}
