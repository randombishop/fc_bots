
parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


def parse_user_instructions(fid_origin=None):
  ans =  """
    INSTRUCTIONS:
    Extract the user name or id from the input.
    Your goal is not to answer the query, you only need to extract the user parameter from the query.
    The query doesn't have to follow a specific format, you just need to extract what you think is most likely the user name or id.
    If you're not sure, pick the first token that starts with a @.

    QUERY EXAMPLES:
    * In input "Who are @alice.eth's favorite users?" -> the user is "alice.eth".
    * In input "randombishop's wordcloud" -> the user is "randombishop".
    * In input "Psycho analyze 328193" -> the user is 328193.
    
    CURRENT_USER_ID?
    
    RESPONSE FORMAT:
    {
      "user": ...
    }
  """
  if fid_origin is not None:
    ans = ans.replace('CURRENT_USER_ID?', f"CURRENT USER ID: {fid_origin}")
  else:
    ans = ans.replace('CURRENT_USER_ID?', '')
  return ans


def concat_casts(posts):
  ans = 'POSTS:\n'
  for post in posts:
    post['id'] = post['hash'][2:8]
    ans += "\n"
    ans += "<"+post['id']+">\n"
    ans += post['text']
    ans += "\n</"+post['id']+">\n"
  ans += "\n"
  return ans
