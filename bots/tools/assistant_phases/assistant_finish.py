from langchain.agents import Tool


def assistant_finish(input):
  return {'log': 'ok'}


AssistantFinish = Tool(
  name="AssistantFinish",
  description="Assistant finish phase",
  func=assistant_finish
)