from langchain.agents import Tool
from bots.utils.skyvern_api import start_workflow, get_workflow_result



skyvern_workflow = "wpid_351323221886267440"


def news(input):
  state = input.state
  if state.action_params is None:
    raise Exception("Missing action_params")
  search = state.action_params['search']
  if search is None or len(search) < 5:
    raise Exception("This action requires a search query to forward to Yahoo News.")
  run_id = start_workflow(skyvern_workflow, {"search": search})
  result = get_workflow_result(skyvern_workflow, run_id)
  if result['status'] != 'completed':
    raise Exception("Workflow did not complete")
  data = result['outputs']['Generate_output']['extracted_information']
  if data is None or 'tweet' not in data:
    raise Exception("Could not get a news story")
  cast = {'text': data['tweet']}
  if 'url' in data and len(data['url']) > 10:
    link = data['url']
    cast['embeds'] = [link]
    cast['embeds_description'] = 'Link to the story'
  casts = [cast]
  state.casts = casts
  return {
    'casts': state.casts
  }


News = Tool(
  name="News",
  description="Get a news story",
  func=news,
  metadata={'depends_on': ['parse_news_params']}
)
