import pandas as pd
import ollama
import gradio as gr
import numpy as np
import os
import hashlib
import pickle
from datetime import datetime

# --- CONFIG ---
DATA_PATH = os.path.join(os.path.dirname(__file__), "assets", "clothes.xlsx")
CACHE_PATH = os.path.join(os.path.dirname(__file__), "assets", "clothes_embeddings.pkl")

#  compute file hash to detect changes ---
def compute_file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# Create embeddings via Ollama ---
def embed_text(text):
    response = ollama.embeddings(model="all-minilm", prompt=text)
    return np.array(response["embedding"])

# - Simplify data and add descriptions ---
def preprocess_dataframe(df):
    cols_to_use = ["Clothes", "Color", "Category", "Occasion", "Size"]
    df_small = df[cols_to_use].copy()
    df_small["description"] = df_small.apply(
        lambda row: f"Item: {row['Clothes']}, Color: {row['Color']}, "
                    f"Category: {row['Category']}, Occasion: {row['Occasion']}, "
                    f"Size: {row['Size']}",
        axis=1,
    )
    return df_small

# --- Generate embeddings for all items ---
def generate_embeddings(df_small):
    print("Generating embeddings for all clothes...")
    df_small["embedding"] = df_small["description"].apply(embed_text)
    print(" Embedding generation complete.")
    return df_small

#  Load or regenerate embeddings depending on Excel changes ---
def load_or_generate_embeddings():
    current_hash = compute_file_hash(DATA_PATH)

    # Check cache
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "rb") as f:
            cache = pickle.load(f)
        cached_hash = cache.get("file_hash")
        if cached_hash == current_hash:
            print("Using cached embeddings (no Excel changes detected).")
            return cache["df"]
        else:
            print("Excel file changed — regenerating embeddings...")

    # If no cache or file changed → regenerate
    df = pd.read_excel(DATA_PATH)
    df_small = preprocess_dataframe(df)
    df_small = generate_embeddings(df_small)

    # Save cache
    with open(CACHE_PATH, "wb") as f:
        pickle.dump({"file_hash": current_hash, "df": df_small}, f)

    print("Cache updated.")
    return df_small

# --- 6. Similarity + LLM chat ---
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_similar_clothes(query, df_small, top_n=5):
    query_emb = embed_text(query)
    df_small["similarity"] = df_small["embedding"].apply(lambda emb: cosine_similarity(emb, query_emb))
    return df_small.nlargest(top_n, "similarity")

def ask_outfit(query, df_small):
    similar_items = find_similar_clothes(query, df_small, top_n=5)
    clothes_text = "\n".join(similar_items["description"].tolist())

    prompt = f"""
You are a fashion assistant. Here are a few relevant clothes:

{clothes_text}

The user asked: "{query}"

Suggest the best outfit (combine top + bottom if possible) based on the user's request.
Make sure the color pattern, eventType, and occasion fit the user's request.
    """

    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

# ---  Gradio Interface ---
def main():
    df_small = load_or_generate_embeddings()

    def chat_fn(user_input):
        return ask_outfit(user_input, df_small)

    gr.Interface(
        fn=chat_fn,
        inputs=gr.Textbox(lines=2, placeholder="Ask about outfits..."),
        outputs="text",
        title="Fashion Buddy (with Smart Embedding Cache)",
        description="Ask for outfits — embeddings update only if Excel changes."
    ).launch()

if __name__ == "__main__":
    main()
