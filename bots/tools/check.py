from langchain.agents import Tool


def _check(state):
  state.checked = True
    

check = Tool(
  name="check",
  description="Check outputs phase",
  func=_check
)