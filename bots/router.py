from bots.parser import parse
from bots.actions.digest_casts import DigestCasts
from bots.actions.favorite_users import FavoriteUsers
from bots.actions.most_active_users import MostActiveUsers
from bots.actions.pick_cast import PickCast
from bots.actions.run_sql import RunSql


actions ={
  'run_sql': RunSql,
  'pick_cast': PickCast,
  'digest_casts': DigestCasts,
  'favorite_users': FavoriteUsers,
  'most_active_users': MostActiveUsers
}


def route(request):
  print('request', request)
  parsed = parse(request)
  print('parsed', parsed)  
  func = parsed['function']
  params = parsed['params']
  Action = actions[func]
  action = Action(params)
  return action

