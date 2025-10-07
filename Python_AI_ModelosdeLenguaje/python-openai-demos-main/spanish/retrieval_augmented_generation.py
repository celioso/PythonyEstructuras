import csv
import os
from pathlib import Path

import azure.identity
import openai
from dotenv import load_dotenv

# Configura el cliente de OpenAI para usar la API de Azure, OpenAI.com u Ollama
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.OpenAI(
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=token_provider,
    )
    MODEL_NAME = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]

elif API_HOST == "ollama":
    client = openai.OpenAI(base_url=os.environ["OLLAMA_ENDPOINT"], api_key="nokeyneeded")
    MODEL_NAME = os.environ["OLLAMA_MODEL"]

elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.github.ai/inference", api_key=os.environ["GITHUB_TOKEN"])
    MODEL_NAME = os.getenv("GITHUB_MODEL", "openai/gpt-4o")

else:
    client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
    MODEL_NAME = os.environ["OPENAI_MODEL"]


USER_MESSAGE = "¿qué tan rápido es el Prius v?"

# Abrir el CSV y almacenar en una lista
CSV_PATH = Path(__file__).with_name("hybridos.csv")
with CSV_PATH.open(newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    rows = list(reader)

# Normalizar la pregunta del usuario para reemplazar puntuación y convertir a minúsculas
normalized_message = USER_MESSAGE.lower().replace("?", "").replace("(", " ").replace(")", " ")

# Buscar en el CSV la pregunta del usuario usando una búsqueda muy simple
words = normalized_message.split()
matches = []
for row in rows[1:]:
    # si la palabra coincide con cualquier palabra en la fila, añadir la fila a las coincidencias
    if any(word in row[0].lower().split() for word in words) or any(word in row[5].lower().split() for word in words):
        matches.append(row)

# Formatear como una tabla markdown, ya que los modelos de lenguaje entienden markdown
matches_table = " | ".join(rows[0]) + "\n" + " | ".join(" --- " for _ in range(len(rows[0]))) + "\n"
matches_table += "\n".join(" | ".join(row) for row in matches)
print(f"Encontradas {len(matches)} coincidencias:")
print(matches_table)

# Ahora podemos usar las coincidencias para generar una respuesta
SYSTEM_MESSAGE = """
Eres un asistente útil que responde preguntas sobre coches basándote en un conjunto de datos de coches híbridos.
Debes usar el conjunto de datos para responder las preguntas,
no debes proporcionar ninguna información que no esté en las fuentes proporcionadas.
"""

response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.3,
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": USER_MESSAGE + "\nFuentes: " + matches_table},
    ],
)

print(f"Respuesta de {API_HOST}: \n")
print(response.choices[0].message.content)
