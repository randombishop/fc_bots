from langchain.agents import Tool
from bots.utils.skyvern_api import start_workflow, get_workflow_result



skyvern_workflow = "wpid_351323221886267440"


def get_news(input):
  state = input.state
  search = state.search
  if search is None or len(search) < 5:
    raise Exception("This action requires a search query to forward to Yahoo News.")
  run_id = start_workflow(skyvern_workflow, {"search": search})
  result = get_workflow_result(skyvern_workflow, run_id)
  if result['status'] != 'completed':
    return {"error": "News Workflow did not complete"}
  state.yahoo_news = result['outputs']['Generate_output']['extracted_information']
  return {
    'yahoo_news': state.yahoo_news
  }


GetNews = Tool(
  name="GetNews",
  description="Get a news story",
  func=get_news
)
