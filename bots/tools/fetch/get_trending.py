from langchain.agents import Tool
from bots.data.casts import get_trending_casts
from bots.utils.format_cast import format_trending


def fetch(input):
  casts = get_trending_casts(50)
  text = format_trending(casts)
  return {'trending': text}


GetTrending = Tool(
  name="GetTrending",
  description="Get the globally trending posts",
  metadata={
    'outputs': ['trending']
  },
  func=fetch
)