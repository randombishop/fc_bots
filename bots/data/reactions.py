from bots.data.bq import execute


fav_usr_sql = """
SELECT 
target_fid, 
(select user_name from fid_username where fid_username.fid=reactions.target_fid) as username,
num_recasts, 
num_likes, 
num_replies 
FROM reactions 
WHERE fid={} AND target_fid!={}
AND (select user_name from fid_username where fid_username.fid=reactions.target_fid) is not null
ORDER BY (3*num_recasts + 2*num_likes + 1*num_replies) DESC
LIMIT 10 ;
"""

def favorite_users_sql(fid):
  return fav_usr_sql.format(fid, fid)

def favorite_users_results(fid):
  sql = favorite_users_sql(fid)
  response = execute(sql)
  results = [x for x in response]
  return results