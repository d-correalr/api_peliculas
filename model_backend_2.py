import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Cargar el modelo ensamblado
with open("modelo_ensamble_final_2.pkl", "rb") as f:
    modelo = pickle.load(f)

clf_sbert = modelo["clf_sbert"]
clf_tfidf = modelo["clf_tfidf"]
vectorizer = modelo["vectorizer"]
mlb = modelo["mlb"]
mejor_peso = modelo["mejor_peso"]
cols = modelo["cols"]

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def predict_genre(year, rating, title, plot):
    texto = plot.lower()

    # Vectorizaciones
    emb = embedder.encode([texto])
    tfidf_vec = vectorizer.transform([texto])

    # Predicciones
    probs_sbert = clf_sbert.predict_proba(emb)
    probs_tfidf = clf_tfidf.predict_proba(tfidf_vec)
    probs_final = mejor_peso * probs_sbert + (1 - mejor_peso) * probs_tfidf
    probs_final = probs_final.flatten()

    # Top 5 géneros
    top_idxs = np.argsort(probs_final)[::-1][:5]
    top_genres = [
        {"genre": cols[i].replace("p_", ""), "probability": float(probs_final[i])}
        for i in top_idxs
    ]

    return {
        "predicted_genre": top_genres[0]["genre"],
        "top_5_genres": top_genres
    }
