from langchain.agents import Tool


phases = [
  'initialize',
  'wakeup',
  'plan',
  'parse',
  'fetch',
  'prepare',
  'combine',
  'check',
  'memorize'
]


def next_phase(input):    
  current = input.state.current_phase
  index = phases.index(current)
  next = phases[index+1]
  input.state.current_phase = next
  return {'current_phase': next}


NextPhase = Tool(
  name="next_phase",
  func=next_phase,
  description="Move on to the next phase of the bot processing pipeline"
)
