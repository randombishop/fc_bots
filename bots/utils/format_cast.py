from datetime import datetime
from bots.utils.check_links import check_link_data
from bots.data.users import get_fid


def concat_casts(posts):
  ans = ''
  for post in posts:
    post['id'] = post['hash'][2:8]
    ans += "\n"
    ans += "<"+post['id']+">\n"
    ans += post['user_name'] + " said: " + post['text']
    ans += "\n</"+post['id']+">\n"
  ans += "\n"
  return ans

def format_when(timestamp):
  if isinstance(timestamp, str):
    timestamp = timestamp.replace('T', ' ')
    timestamp = timestamp[:19]
    timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    timestamp_seconds = timestamp_dt.timestamp()
  elif isinstance(timestamp, datetime):
    timestamp_seconds = timestamp.timestamp()
  else:
    timestamp_seconds = int(timestamp) / 1000
  now = datetime.now()
  timestamp_dt = datetime.fromtimestamp(timestamp_seconds)
  delta = now - timestamp_dt
  if delta.days > 0:
    return f"{delta.days} days ago"
  hours = delta.seconds // 3600
  if hours > 0:
    return f"{hours} hours ago"
  minutes = delta.seconds // 60
  if minutes > 0:
    return f"{minutes} minutes ago"
  return "seconds ago"

def insert_mentions(original: str, mentions: list[str], mention_positions: list[int]) -> str:
  if len(mentions) != len(mention_positions):
    raise ValueError("Mentions and positions arrays must have the same length")
  # Step 1: Encode the original string to UTF-8 bytes
  utf8_bytes = original.encode('utf-8')
  # Step 2: Cut the byte array at specified positions
  parts = []
  start = 0
  for pos in mention_positions:
    parts.append(utf8_bytes[start:pos])
    start = pos
  parts.append(utf8_bytes[start:])  # Add the last part
  # Step 3: Reconvert the byte parts to strings
  result_parts = [part.decode('utf-8') for part in parts]
  # Step 4: Insert the mentions between the parts
  result = result_parts[0]
  for i in range(len(mentions)):
    result += mentions[i] + result_parts[i + 1]
  return result

def extract_mentions(text):
  if text is None:
    return '', [], []    
  mentions = []
  positions = []
  result_text = ''
  i = 0
  while i < len(text):
    if text[i] == '@':
      mention_start = i
      i += 1
      while i < len(text) and (text[i].isalnum() or text[i] == '_' or text[i] == '.'):
        i += 1
      mention = text[mention_start:i]
      if len(mention) > 1: 
        mentions.append(mention)
        positions.append(len(result_text.encode('utf-8')))
      else:
        result_text += '@'
    else:
      result_text += text[i]
      i += 1
  return result_text, mentions, positions

def shorten_text(text):
  if text is None:
    return ''
  text_lines = text.split('\n')
  if len(text_lines) > 1:
    text = text_lines[0] + '...'
  if len(text) > 256:
    text = text[:256]+'...'
  return text

def format_casts(casts):
  if casts is None or len(casts)==0:
    return ''
  ans = ''
  for c in casts:
    text = c['text']
    if 'mentions_ats' in c and 'mentions_pos' in c:
      text = insert_mentions(text, c['mentions_ats'], c['mentions_pos'])
    ans += f"> {text}"
    if 'embeds' in c and c['embeds'] is not None and len(c['embeds'])>0:
      embed = c['embeds'][0]
      description = c['embeds_description'] if 'embeds_description' in c else None
      description = shorten_text(description)
      if 'user_name' in embed and 'hash' in embed:
        ans += f" [{description}](https://warpcast.com/{embed['user_name']}/{embed['hash'][:10]})"
      else:
        ans += f" [{description}]({embed})"
    ans += '\n'
  return ans

def extract_cast(result, posts_map, index=''):
  text = result[f'tweet{index}'] if f'tweet{index}' in result else None
  if text is None:
    text = ''
  embed_url = result[f'embed_url{index}'] if f'embed_url{index}' in result else None
  embed_hash = result[f'embed_hash{index}'] if f'embed_hash{index}' in result else None
  if len(text)==0 and embed_url is None and embed_hash is None:
    return None
  c = {'text': text}
  if embed_url is not None:
    c['embeds'] = [embed_url]
    c['embeds_description'] = 'link'
  elif embed_hash is not None:
    link = check_link_data({'id': embed_hash}, posts_map)
    if link is not None:
      c['embeds'] = [{'fid': link['fid'], 'user_name': link['user_name'], 'hash': link['hash']}],
      c['embeds_description'] = link['text']
      c['embeds_warpcast'] = f"https://warpcast.com/{link['user_name']}/{link['hash'][:10]}"
  raw_text, mentions_ats, mentions_positions = extract_mentions(c['text'])
  if len(mentions_ats) > 0:
    mentions = [get_fid(x[1:]) for x in mentions_ats]
    mentions = [int(x) for x in mentions if x is not None]
    if len(mentions) == len(mentions_ats):
      c['text'] = raw_text
      c['mentions'] = mentions
      c['mentions_ats'] = mentions_ats
      c['mentions_pos'] = mentions_positions
  return c