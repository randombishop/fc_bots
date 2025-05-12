from bots.kit_interface.user_id import UserId
from bots.kit_interface.miniapp import MiniApp


def get_avatar_match(user_id: UserId) -> MiniApp:
  return MiniApp("https://ava.datascience.art/")