from dotenv import load_dotenv
load_dotenv()
import sys
import re
from bots.iaction import IAction
from bots.data.casts import get_cast, get_more_like_this


class MoreLikeThis(IAction):

  def set_input(self, input):
    params = {}
    if self.attachment_hash is not None:
      attached_cast = get_cast(self.attachment_hash)
      params['text'] = attached_cast['text']
    elif self.parent_hash is not None:
      parent_cast = get_cast(self.parent_hash)
      params['text'] = parent_cast['text']
    else:
      text = re.sub(r'(?i)more like this:?', '', input).strip()
      params['text'] = text
    self.input = input
    self.set_params(params)

  def set_params(self, params):
    self.text = params['text']
    if self.text is None or len(self.text) < 5:
      raise Exception("This action requires some text to find similar posts.")

  def get_cost(self):
    self.cost = 20
    return self.cost

  def get_data(self):
    exclude_hash = None
    if self.attachment_hash is not None:
      exclude_hash = self.attachment_hash
    elif self.parent_hash is not None:
      exclude_hash = self.parent_hash
    similar = get_more_like_this(self.text, exclude_hash=exclude_hash, limit=3)
    if len(similar) == 0:
      raise Exception("No similar posts found.")
    self.data = similar.to_dict(orient='records')
    return self.data

  def get_casts(self, intro=''):
    casts = []
    for similar in self.data:
      casts.append({'text': '', 'embeds': [{'fid': similar['fid'], 'user_name': similar['user_name'], 'hash': similar['hash']}]})
    self.casts = casts
    return self.casts
