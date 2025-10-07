import os

import azure.identity
import openai
from dotenv import load_dotenv

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
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


SYSTEM_MESSAGE = """
You are a helpful assistant that helps students with their homework.
Instead of providing the full answer, you respond with a hint or a clue.
"""


USER_MESSAGE = "What is the largest planet in our solar system?"


response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.7,
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "Can you remember the name of the city that is known for the Eiffel Tower?"},
        {"role": "user", "content": "What is the square root of 144?"},
        {"role": "assistant", "content": "What number multiplied by itself equals 144?"},
        {"role": "user", "content": "What is the atomic number of oxygen?"},
        {"role": "assistant", "content": "How many protons does an oxygen atom have?"},
        {"role": "user", "content": USER_MESSAGE},
    ],
)


print(f"Response from {API_HOST}: \n")
print(response.choices[0].message.content)
