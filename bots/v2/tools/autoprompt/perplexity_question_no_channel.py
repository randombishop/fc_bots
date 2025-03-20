from langchain.agents import Tool
from bots.v2.call_llm import call_llm


prompt_template = """
#TRENDING POSTS FROM EVERYONE
{{casts_in_channel}}

#YOUR POSTS IN THE CHANNEL
{{bot_casts_no_channel}}
"""

instructions_template = """
You are @{{name}} social media bot running on the Farcaster platform.
Your task is to come up with a new original and interesting question for the farcaster community.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#INSTRUCTIONS
You are provided with recent trending activity in the farcaster social media platform.
First, read these posts carefully and summarize them in one short paragraph.
Then generate a new question that will be forwarded to an AI to prepare your next post.
Your question should be simple, short, original, interesting and creative.
Your question should be genuine: what would YOU like to know if you had access to a powerful AI and recent news?
Do not generate multiple questions or complex questions.
Please generate only one single, simple and short question.
Do not copy existing posts.
Do not re-use your previous questions.
Output your decision in JSON format.
Make sure you don't use " inside json strings. Avoid invalid json.

#RESPONSE FORMAT:
{
  "current_trends_summary": "one short paragraph summarizing the current trends",
  "question": "short question to forward to another AI",
  "reasoning": "explain why you picked this question."
}
"""

schema = """
  "type":"OBJECT",
  "properties":{
    "current_trends_summary":{"type":"STRING"},
    "question":{"type":"STRING"},
    "reasoning":{"type":"STRING"}
"""

def perplexity_question_no_channel(input):
  state = input['state']
  llm = input['llm']
  prompt = state.format(prompt_template)
  instructions = state.format(instructions_template)
  result = call_llm(llm, prompt, instructions, schema)
  question = result['question'] if 'question' in result else None
  current_trends_summary = result['current_trends_summary'] if 'current_trends_summary' in result else None
  reasoning = result['reasoning'] if 'reasoning' in result else None
  log = 'Trends: '+current_trends_summary+'\n'+'Reasoning: '+reasoning
  return {
    'question': question,
    'log': log
    }


PerplexityQuestionNoChannel = Tool(
  name="perplexity_question_no_channel",
  description="Generate a question for the perplexity action in main feed",
  func=perplexity_question_no_channel,
  metadata={
    'depends_on': ['get_trending', 'get_bot_casts_no_channel']
  }
)
