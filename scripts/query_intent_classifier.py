from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class QueryIntentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=500
        )

        self.model = LogisticRegression(
            max_iter=1000,
            random_state=42
        )

    def train(self, queries, labels):
        X = self.vectorizer.fit_transform(queries)
        self.model.fit(X, labels)

    def predict(self, query):
        X = self.vectorizer.transform([query])

        probabilities = self.model.predict_proba(X)[0]

        best_index = probabilities.argmax()

        intent = self.model.classes_[best_index]
        confidence = probabilities[best_index]

        return intent, confidence