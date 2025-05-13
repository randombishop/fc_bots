import re
from bots.data.users import get_fid
from bots.utils.format_when import format_when
from bots.utils.shorten import MAX_LENGTH, shorten_text, cut_text


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
      while i < len(text) and (text[i].isalnum() or text[i] == '_' or text[i] == '.' or text[i] == '-'):
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
  mention_ats = [clean_username(x) for x in mentions]
  return result_text, mention_ats, positions


def clean_username(username):
  if username is not None and len(username) > 0 and username[-1] in '.!?,;:':
    username = username[:-1]
  return username


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
      description = cut_text(description)
      if 'user_name' in embed and 'hash' in embed:
        ans += f" [{description}](https://warpcast.com/{embed['user_name']}/{embed['hash'][:10]})"
      else:
        ans += f" [{description}]({embed})"
    ans += '\n'
  return ans


def extract_links(text):
  link_pattern = r'\[(.*?)\]'
  links = re.findall(link_pattern, text)
  text_without_links = re.sub(link_pattern, '', text)
  links = [replace_warpcast_links(x) for x in links]
  return text_without_links, links


def replace_warpcast_links(link):
  if 'warpcast.com' in link:
    idx = link.rfind('/')
    if idx != -1:
      id = link[idx+1:]
      if id.startswith('0x'):
        if len(id) > 8:
          id = id[:8]
        return id
  return link


def clean_text(text):
  if text is None:
    return None
  text = text.replace('$', '')
  text = text.replace('tweet', 'cast')
  if len(text) > 2:
    if text[0]=='"':
      text = text[1:]
    if text[-1]=='"':
      text = text[:-1]
  return text


def exclude_link(x):
  exclude = ['warpcast.com', 'www.dsart.io']
  for e in exclude:
    if e in x:
      return True
  return False

def extract_cast(text, posts_map, style):
  text, links = extract_links(text)
  embed_urls = [x for x in links if x.startswith('https://') or x.startswith('http://')]
  embed_urls = [x for x in embed_urls if not exclude_link(x)]
  embed_hashes = [x for x in links if x.startswith('0x')]
  if len(text) > MAX_LENGTH:
    text = shorten_text(text, style)
  text = clean_text(text)
  text, mentions_ats, mentions_positions = extract_mentions(text)
  print('mentions_ats', mentions_ats)
  print('mentions_positions', mentions_positions)
  c = {'text': text}
  if embed_urls is not None and len(embed_urls) > 0:
    c['embeds'] = embed_urls
    c['embeds_description'] = 'link'
  if embed_hashes is not None and len(embed_hashes) > 0:
    link = posts_map[embed_hashes[0]] if embed_hashes[0] in posts_map else None
    if link is not None:
      embed0 = {
        'fid': link.fid, 
        'user_name': link.username, 
        'hash': link.hash
      }
      c['embeds'] = [embed0]
      c['embeds_description'] = link.text
      c['embeds_warpcast'] = f"https://warpcast.com/{link.username}/{link.hash[:10]}"
  if len(mentions_ats) > 0:
    try:
      mentions = [get_fid(x[1:]) for x in mentions_ats]
      mentions = [int(x) for x in mentions if x is not None]
      if len(mentions) == len(mentions_ats):
        c['mentions'] = mentions
        c['mentions_ats'] = mentions_ats
        c['mentions_pos'] = mentions_positions
    except:
      pass
  return c


def format_bot_casts(casts, name):
  text = ''
  for c in casts:
    row = f'## @{name} posted'
    if c['action_channel'] is not None:
      row += f" in {c['action_channel']}"
    row += f" {format_when(c['casted_at'])}:\n"
    row += f"{cut_text(c['casted_text'])}\n"
    text += row+'\n'
  return text


def format_trending(casts):
  text = ''
  for s in casts:
    cast_text = s['text']
    if cast_text is None:
      cast_text = ''
    else:
      cast_text = cast_text.replace('\n', ' ')
      if len(cast_text) > 500:
        cast_text = cast_text[:500]+'...'
    row = f"## @{s['username']} posted {format_when(s['timestamp'])}:\n{cut_text(cast_text)}"
    if s['embed_text'] is not None and len(s['embed_text']) > 0:
      embed_text = cut_text(s['embed_text'])
      embed_username = s['embed_username']
      row += f" (quoting @{embed_username}: {embed_text})"
    row += '\n'
    text += row+'\n'
  return text