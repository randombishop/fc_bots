import os
from bots.kit_interface.source_code import SourceCode


def _get_source_code(folder, file, package):
  ans = ''
  current_dir = os.path.dirname(os.path.abspath(__file__))
  state_file = os.path.join(current_dir, folder, file)
  with open(state_file, 'r') as f:
    ans += f"### {package}.{file[:-3]} ###'\n"
    ans += f.read() + '\n'
    ans += f"### End of {file} ###'\n"
  return ans


def get_source_code() -> SourceCode:
  ans = ''
  ans += _get_source_code('../../kit_entrypoint', 'fetch.py', 'bots.kit_entrypoint') + '\n'
  ans += _get_source_code('../../kit_entrypoint', 'prepare.py', 'bots.kit_entrypoint') + '\n'
  ans += _get_source_code('../../kit_entrypoint', 'miniapps.py', 'bots.kit_entrypoint') + '\n'
  ans += _get_source_code('../..', 'state.py', 'bots') + '\n\n'
  return SourceCode(ans)
