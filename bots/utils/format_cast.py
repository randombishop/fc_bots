

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