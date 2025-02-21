import requests
import os


URL = "https://api.perplexity.ai/chat/completions"
TOKEN = os.getenv("PERPLEXITY_API_KEY")
MODEL = "sonar"
SYSTEM_PROMPT = "Answer with one short tweet. Do not use hashtags. Generate an original and engaging tweet. Keep it short and to the point."

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
    "max_tokens": 512,
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

