from datetime import datetime, timedelta
from bots.data.wield import get_cast_info
from bots.data.dune import run_query
from dune_client.types import QueryParameter


def get_casts_for_fid(fid):
  query_id = 4248613
  params = [QueryParameter.number_type(name="fid", value=fid)]
  return run_query(query_id, params)

def get_top_casts(channel, keyword, category, max_rows):
  query_id = 4252915
  params = [
    QueryParameter.text_type(name="parent_url", value=channel if channel is not None else '*'),
    QueryParameter.text_type(name="keyword", value=keyword if keyword is not None else '*'),
    QueryParameter.text_type(name="category", value=category if category is not None else '*'),
    QueryParameter.number_type(name="limit", value=max_rows)
  ]
  return run_query(query_id, params)
  
def get_cast(hash):
  cast = get_cast_info(hash)
  return {
    'fid': int(cast['author']['fid']),
    'text': cast['text'],
    'mentions': cast['mentions'] if 'mentions' in cast else [], 
    'mentionsPos': cast['mentionsPositions'] if 'mentionsPositions' in cast else [],
    'parent_fid': cast['parentFid'] if 'parentFid' in cast else None,
    'parent_hash': cast['parentHash'] if 'parentHash' in cast else None
  }
  