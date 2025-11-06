import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "models"
MODEL_PATH.mkdir(exist_ok=True)

class NLUEvaluator:
    def __init__(self):
        self.vec = TfidfVectorizer(ngram_range=(1,2))
        self.model = LogisticRegression(max_iter=250)
        self._trained = False
        self.model_file = MODEL_PATH / "nlu_model.pkl"
        if self.model_file.exists():
            self._load()

    def _train_default(self):
        X = [
            "turn on the living room light","switch on lights",
            "turn off the light","turn off the kitchen lights",
            "lock the front door","unlock the door",
            "open the garage","close the garage",
            "turn on the fan","turn off the fan",
            "goodnight","good morning"
        ]
        y = [
            "light_on","light_on",
            "light_off","light_off",
            "lock","unlock",
            "open_garage","close_garage",
            "fan_on","fan_off",
            "goodnight","goodmorning"
        ]
        Xv = self.vec.fit_transform(X)
        self.model.fit(Xv, y)
        self._trained = True
        self._save()

    def _save(self):
        with open(self.model_file, "wb") as f:
            pickle.dump({"vec": self.vec, "model": self.model}, f)

    def _load(self):
        with open(self.model_file, "rb") as f:
            data = pickle.load(f)
            self.vec = data["vec"]
            self.model = data["model"]
            self._trained = True

    def ensure_trained(self):
        if not self._trained:
            self._train_default()

    def predict(self, text: str):
        self.ensure_trained()
        Xv = self.vec.transform([text])
        intent = self.model.predict(Xv)[0]
        probs = self.model.predict_proba(Xv)[0]
        scores = dict(zip(self.model.classes_, probs))
        return {"intent": intent, "scores": scores}
