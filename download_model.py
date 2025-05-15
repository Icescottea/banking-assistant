# download_model.py
import requests
import os

url = "https://huggingface.co/ICESCOTTEA/banking-assistant-models/resolve/main/transformer_intent_model.pkl"
output_path = "models/transformer_intent_model.pkl"

os.makedirs("models", exist_ok=True)
print("Downloading model...")
r = requests.get(url)
with open(output_path, "wb") as f:
    f.write(r.content)
print("Download complete.")
