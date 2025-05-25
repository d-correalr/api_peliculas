import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Cargar modelo
with open("modelo_tfidf.pkl", "rb") as f:
    modelo = pickle.load(f)

clf = modelo["clf"]
vectorizer = modelo["vectorizer"]
cols = modelo["cols"]

def predict_genre(year, rating, title, plot):
    texto = plot.lower()
    vec = vectorizer.transform([texto])
    probs = clf.predict_proba(vec)[0]
    top_idxs = np.argsort(probs)[::-1][:5]
    top_genres = [
        {"genre": cols[i].replace("p_", ""), "probability": float(probs[i])}
        for i in top_idxs
    ]
    return {
        "predicted_genre": top_genres[0]["genre"],
        "top_5_genres": top_genres
    }
