from bots.i_action_step import IActionStep
from bots.utils.llms import call_llm
from bots.utils.check_links import check_link_data

chat_instructions_template = """
You are @{{name}}, a social media bot.
Your goal is to reply to a user conversation with a creative tweet with a reference to one of the provided posts.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#CURRENT CHANNEL
{{channel}}

#TASK
Respond to the user conversation with a tweet and a link to a post.
Pick a post from the provided ones that is somehow related to the conversation.
Pick a post that has a meaningful, metaphorical, humorous, or even contrasting connection to the conversation.
The selected post doesn't have to be directly related to the conversation, it can be any idea that you can play with when replying to the user.
You can also select a post that connects another user to the conversation and tweet a haiku for both of them.
Be creative in picking a post and select one that will be useful to include in your answer.
Once you found the ideal post to use, respond to the user conversation with a tweet and a link to the post.
If you can't find any post that can be used that way, respond with a tweet only and no link.

#RESPONSE FORMAT
{
  "tweet": "...",
  "link_id": "relevant post id"
}
"""


chat_prompt_template = """
##Posts from @{{user_origin}}
{{about_user}}

##Posts about {{topic}}
{{about_topic}}

##Posts about {{keyword}}
{{about_keyword}}

##Posts about {{context}}
{{about_context}}

#Conversation (this is the current conversation you are having with the user)
{{conversation}}

#Last message (this is the message you are responding to)
{{request}}
"""


chat_schema = {
  "type":"OBJECT",
  "properties":{
    "tweet":{"type":"STRING"},
    "link_id":{"type":"STRING"}
  }
}


class Chat(IActionStep):
    
  def get_prepare_steps(self):
    return ['ShouldContinue', 'GetCasts']
  
  def get_cost(self):
    return 20
    
  def parse(self):
    pass

  def execute(self):
    if not self.state.should_continue:  
      self.state.casts = []
      return
    chat_prompt = self.state.format(chat_prompt_template)
    chat_instructions = self.state.format(chat_instructions_template)
    result = call_llm(chat_prompt, chat_instructions, chat_schema)
    if 'tweet' not in result or result['tweet'] is None or len(result['tweet']) < 2:
      raise Exception('Could not generate a response.')
    link = None
    if 'link_id' in result:
      link = check_link_data({'id':result['link_id']}, self.state.posts_map)
    cast = {
      'text': result['tweet'],
      'embeds': [{'fid': link['fid'], 'user_name': link['user_name'], 'hash': link['hash']}],
      'embeds_description': link['text']
    } 
    casts = [cast]
    self.state.casts = casts
