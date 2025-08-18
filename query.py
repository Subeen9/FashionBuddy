import pandas as pd
import ollama
import gradio as gr
import os
# Load excel data
path = os.path.join(os.path.dirname(__file__), "assets", "clothes.xlsx")
df = pd.read_excel(path)
print(df.head())

#Build clothes_text
clothes_text = ""
for _, row in df.iterrows():
    clothes_text += (
        f"Item: {row['Clothes']}, "
        f"Color: {row['Color']}, "
        f"Category: {row['Category']}, "
        f"Outdoor: {row['Outdoor']}, "
        f"Size: {row['Size']}, "
        f"Tshirt: {row['Tshirt']}, "
        f"Pant: {row['PANT']}, "
        f"Hoodie: {row['Hoodie']}, "
        f"Business: {row['Business']}, "
        f"Occasion: {row['Ocassion']}\n"
    )
# Asking ollama
def ask_outfit(query: str):
    prompt = f"""
You are a fashion assistant. Here are the clothes available:

{clothes_text}

The user asked: "{query}"

Suggest the best outfit (combine top + bottom if possible) based on the user's request. Make sure the color pattern, eventType, ocassion fits the user's request.
    """
    response = ollama.chat(
        model="phi3:mini", 
        messages=[{"role": "user", "content": prompt}]
    )
    print(response)
    return response["message"]["content"]

# UI
def chat_fn(user_input):
    return ask_outfit(user_input)

if __name__ == "__main__":
    gr.Interface(
        fn=chat_fn,
        inputs=gr.Textbox(lines=2, placeholder="Ask about outfits..."),
        outputs="text",
        title="Fashion Buddy",
        description="Ask me what to wear! I analyze your Excel clothes data."
    ).launch()
