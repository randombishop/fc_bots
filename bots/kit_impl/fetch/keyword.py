from bots.utils.read_params import read_keyword
from bots.kit_interface.keyword import Keyword


def new_keyword(keyword: str) -> Keyword:
  params = {'keyword': keyword}
  keyword = read_keyword(params)
  return Keyword(keyword)


def generate_keyword() -> Keyword:
  return new_keyword('')