
parse_user_instructions = """
INSTRUCTIONS:
Find the user referenced in the query.
Your goal is not to answer the query, you only need to extract the user parameter from the query.
The query doesn't have to follow a specific format, you just need to extract what you think is most likely the user name or id.
If you're not sure, pick the first token that starts with a @.

RESPONSE FORMAT:
{
  "user": ...
}
"""

parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}



def concat_casts(posts):
  ans = 'POSTS:\n'
  for post in posts:
    post['id'] = post['hash'][2:8]
    ans += "\n"
    ans += "<"+post['id']+">\n"
    ans += post['user_name'] + " said: " + post['text']
    ans += "\n</"+post['id']+">\n"
  ans += "\n"
  return ans
