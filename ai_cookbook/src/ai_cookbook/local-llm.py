import requests
from openai import OpenAI

ollama_base_url = "http://localhost:11434"
llama_base_url = "http://localhost:11434/v1"
# response = requests.post(
#     "http://localhost:11434/api/generate",
#     json={
#         "model": "gpt-oss",
#         "prompt": "Write an assay about Python",
#         "stream": "False",
#     },
# )

# Check if ollama is responding
# response = requests.get(ollama_base_url)
# print(response.content)

ollama = OpenAI(base_url=llama_base_url, api_key="dummy")

response = ollama.chat.completions.create(
    model="llama3.2", messages=[{"role": "user", "content": "Tell me a fun fact"}]
)

print(response.choices[0].message.content)
