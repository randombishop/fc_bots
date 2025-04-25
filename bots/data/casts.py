from bots.data.dune import run_query
from bots.models.bert import bert
from bots.models.gambit import gambit, categories, topics
from bots.utils.format_when import format_when
from dune_client.types import QueryParameter
from bots.data.pg import get_session
from sqlalchemy import text


def get_top_casts(channel=None, keyword=None, category=None, user_name=None, max_rows=10):
  query_id = 4252915
  params = [
    QueryParameter.text_type(name="parent_url", value=channel if channel is not None else '*'),
    QueryParameter.text_type(name="keyword", value=keyword if keyword is not None else '*'),
    QueryParameter.text_type(name="category", value=category if category is not None else '*'),
    QueryParameter.text_type(name="user_name", value=user_name if user_name is not None else '*'),
    QueryParameter.number_type(name="limit", value=max_rows)
  ]
  return run_query(query_id, params)

def get_more_like_this(text, exclude_hash=None, limit=10):
  embedding = bert([text])
  features = gambit(embedding)
  features['category_label'] = features[categories].idxmax(axis=1)
  features['topic_label'] = features[topics].idxmax(axis=1)
  features = features.to_dict(orient='records')[0]
  features_q = [x for x in features.keys() if x.startswith('q_')]
  features_dim = [x for x in features.keys() if x.startswith('dim_')]
  query_id = 4302734
  params = [
    QueryParameter.text_type(name="category", value=features['category_label']),
    QueryParameter.text_type(name="topic", value=features['topic_label']),
    QueryParameter.number_type(name="limit", value=limit)
  ]
  for f in features_q+features_dim:
    params.append(QueryParameter.number_type(name=f, value=features[f]))
  if exclude_hash is not None:
    params.append(QueryParameter.text_type(name="exclude_hash", value=exclude_hash))
  return run_query(query_id, params)


  
def get_trending_casts(limit=100):
  with get_session() as session:
    sql = text("""
    SELECT *
    FROM ds.trending_casts
    ORDER BY timestamp DESC
    LIMIT :limit
    """)
    result = session.execute(sql, {'limit': limit})
    return result.mappings().all()
  

def get_user_replies_and_reactions(fid, max_rows=25):
  query_id = 4762421
  params = [
    QueryParameter.number_type(name="fid", value=fid),
    QueryParameter.number_type(name="limit", value=max_rows)
  ]
  return run_query(query_id, params)