import requests
import os


URL = "https://api.perplexity.ai/chat/completions"
TOKEN = os.getenv("PERPLEXITY_API_KEY")
MODEL = "sonar-reasoning"
SYSTEM_PROMPT = "Answer with one short tweet."

def call_perplexity(question):
  payload = {
    "model": MODEL,
    "messages": [
      {
          "role": "system",
          "content": SYSTEM_PROMPT
      },
      {
          "role": "user",
          "content": 'Answer the following question with one short tweet: ' + question
      }
    ],
    "max_tokens": 256,
    "return_images": False,
    "return_related_questions": False,
    "search_recency_filter": "week",
    "stream": False
  }
  headers = {
    "Authorization": "Bearer "+TOKEN,
    "Content-Type": "application/json"
  }
  response = requests.request("POST", URL, json=payload, headers=headers)
  return response.json()

