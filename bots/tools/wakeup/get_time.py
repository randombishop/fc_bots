from datetime import datetime
from langchain.agents import Tool


def get_time(input):
  state = input.state
  state.time = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
  return {'time': state.time}

GetTime = Tool(
  name="GetTime",
  func=get_time,
  description="Get the current date and time."
)
