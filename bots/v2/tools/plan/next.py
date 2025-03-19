from langchain.agents import Tool


def next(state):
  pass


Next = Tool(
  name="_",
  func=next,
  description="Move to next step"
)
