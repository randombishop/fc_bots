from bots.i_prepare_step import IPrepareStep
from bots.data.casts import get_trending_casts
from bots.utils.format_cast import format_when, shorten_text


class GetTrending(IPrepareStep):
    
  def prepare(self):
    casts = get_trending_casts(50)
    text = ''
    for s in casts:
      cast_text = s['text']
      if cast_text is None:
        cast_text = ''
      else:
        cast_text = cast_text.replace('\n', ' ')
        if len(cast_text) > 500:
          cast_text = cast_text[:500]+'...'
      row = f"@{s['username']} posted {format_when(s['timestamp'])}: {shorten_text(cast_text)}"
      if s['embed_text'] is not None and len(s['embed_text']) > 0:
        embed_text = shorten_text(s['embed_text'])
        embed_username = s['embed_username']
        row += f" (quoting @{embed_username}: {embed_text})"
      row += '\n'
      text += row
    self.state.trending = text
