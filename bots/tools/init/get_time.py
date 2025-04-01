from datetime import datetime
from langchain.agents import Tool


def get_time(input):
  time = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
  return {'time': time}

GetTime = Tool(
  name="GetTime",
  func=get_time,
  description="Get the current date and time."
)
