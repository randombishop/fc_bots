from datetime import datetime


def format_when(timestamp):
  if isinstance(timestamp, str):
    timestamp_dt = None
    try:
      timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
      try:
        timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
      except ValueError:
        timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
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

def shorten_text(text):
  if text is None:
    return ''
  text_lines = text.split('\n')
  if len(text_lines) > 1:
    text = text_lines[0] + '...'
  if len(text) > 256:
    text = text[:256]+'...'
  return text

