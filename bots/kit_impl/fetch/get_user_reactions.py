from bots.kit_interface.reaction import Reaction
from bots.kit_interface.reactions import Reactions
from bots.data.neynar import get_user_replies_and_recasts, get_user_likes


def get_user_reactions(fid: int) -> Reactions:
  data = []
  replies_recasts = get_user_replies_and_recasts(fid, 25)
  likes = get_user_likes(fid, 25)
  if replies_recasts is not None:
    data += replies_recasts
  if likes is not None:
    data += likes
  if len(data) == 0:
    return None
  data.sort(key=lambda x: x['timestamp'])
  reactions = [Reaction(x) for x in data]
  return Reactions(reactions)

