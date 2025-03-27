from langchain.agents import Tool
from bots.utils.skyvern_api import start_workflow, get_workflow_result



skyvern_workflow = "wpid_351323221886267440"


def fetch(input):
  state = input.state
  search = state.get('search')
  if len(search) < 5:
    raise Exception("This action requires a search query to forward to Yahoo News.")
  run_id = start_workflow(skyvern_workflow, {"search": search})
  result = get_workflow_result(skyvern_workflow, run_id)
  if result['status'] != 'completed':
    return {"error": "News Workflow did not complete"}
  yahoo_news_data = result['outputs']['Generate_output']['extracted_information']
  if 'tweet' not in yahoo_news_data:
    raise Exception("Invalid data")
  yahoo_news = yahoo_news_data['tweet'] + "\n" + yahoo_news_data['url']
  return {
    'yahoo_news': yahoo_news,
    'data_yahoo_news': yahoo_news_data
  }


GetNews = Tool(
  name="GetNews",
  description="Get a news story",
  metadata={
    'inputs': ['search'],
    'outputs': ['yahoo_news', 'data_yahoo_news']
  },
  func=fetch
)
