from bots.kit_interface.casts import Casts


def aggregate_casts(description: str, cast_lists: list[Casts]):
  casts = []
  for cast_list in cast_lists:
    if cast_list is not None:
      casts.extend(cast_list.casts)
  if len(casts) == 0:
    return None
  casts.sort(key=lambda x: x.timestamp) 
  return Casts(description, casts)
