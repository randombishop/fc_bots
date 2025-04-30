from bots.kit_interface.news import News
from bots.utils.skyvern_api import start_workflow, get_workflow_result


skyvern_workflow = "wpid_351323221886267440"


def get_news(search: str) -> News:
  if len(search) < 5:
    raise Exception("This action requires a search query to forward to Yahoo News.")
  run_id = start_workflow(skyvern_workflow, {"search": search})
  result = get_workflow_result(skyvern_workflow, run_id)
  if result['status'] != 'completed':
    return {"error": "News Workflow did not complete"}
  yahoo_news_data = result['outputs']['Generate_output']['extracted_information']
  if 'tweet' not in yahoo_news_data:
    raise Exception("Invalid data")
  return News(yahoo_news_data['tweet'], yahoo_news_data['url'])

