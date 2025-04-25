from datetime import datetime


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