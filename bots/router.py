import sys
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


if __name__ == "__main__":
  request = sys.argv[1]
  action = route(request)
  print(action)
  action.get_cost()
  print(f"Cost: {action.cost}")
  action.execute()
  print(f"Data: {action.data}")
  action.get_casts()
  print(f"Casts: {action.casts}")