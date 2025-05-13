# Data interfaces
from bots.kit_interface.capabilities_examples import CapabilitiesExamples
from bots.kit_interface.casts import Casts
from bots.kit_interface.channel_id import ChannelId
from bots.kit_interface.data_frame import DataFrame
from bots.kit_interface.dune_query import DuneQuery
from bots.kit_interface.favorite_users import FavoriteUsers
from bots.kit_interface.keyword import Keyword
from bots.kit_interface.most_active_users import MostActiveUsers
from bots.kit_interface.news import News
from bots.kit_interface.reactions import Reactions
from bots.kit_interface.search_phrase import SearchPhrase
from bots.kit_interface.source_code import SourceCode
from bots.kit_interface.user_id import UserId
from bots.kit_interface.user_info import UserInfo
# Tool implementations
from bots.kit_impl.fetch.get_capabilities import get_capabilities_examples
from bots.kit_impl.fetch.get_source_code import get_source_code
from bots.kit_impl.fetch.get_channel_id import get_channel_id
from bots.kit_impl.fetch.get_user_id import get_user_id
from bots.kit_impl.fetch.get_random_user import get_random_user_in_channel, get_random_user_in_general
from bots.kit_impl.fetch.get_user_info import get_user_info
from bots.kit_impl.fetch.get_news import get_news
from bots.kit_impl.fetch.get_favorite_users import get_favorite_users
from bots.kit_impl.fetch.get_most_active_users import get_most_active_users
from bots.kit_impl.fetch.get_casts_channel import get_casts_channel
from bots.kit_impl.fetch.get_casts_keyword import get_casts_keyword
from bots.kit_impl.fetch.get_casts_search import get_casts_search
from bots.kit_impl.fetch.get_casts_user import get_casts_user
from bots.kit_impl.fetch.aggregate_casts import aggregate_casts 
from bots.kit_impl.fetch.get_bot_casts_in_channel import get_bot_casts_in_channel
from bots.kit_impl.fetch.get_bot_casts_all import get_bot_casts_all
from bots.kit_impl.fetch.get_trending import get_trending
from bots.kit_impl.fetch.get_user_reactions import get_user_reactions
from bots.kit_impl.fetch.make_cast_stats_sql_query import make_cast_stats_sql_query
from bots.kit_impl.fetch.make_user_stats_sql_query import make_user_stats_sql_query
from bots.kit_impl.fetch.execute_dune_query import execute_dune_query
from bots.kit_impl.fetch.keyword import new_keyword, generate_keyword
from bots.kit_impl.fetch.search_phrase import new_search_phrase, generate_search_phrase
# utils
from bots.utils.format_state import format_state

class Fetch:
  
  def __init__(self, state):
    self.state = state
    
  def get_capabilities_examples(self) -> CapabilitiesExamples:
    """
    Get examples of tasks that can be performed using your tools.
    
    Returns:
        CapabilitiesExamples: A CapabilitiesExamples object containing the examples of tasks that can be performed using your tools.
    """
    return get_capabilities_examples()
  
  def get_source_code(self) -> SourceCode:
    """
    Get the source code of the bot.
    
    Returns:
        SourceCode: A SourceCode object containing your python implementation.
    """
    return get_source_code()

  def get_channel_id(self, parsed_channel: str) -> ChannelId:
    """
    Get the parameters channel_url and channel to run the channel related tools.
    Use get_channel_id when you need to convert channel information to the correct id compatible with your tools.
    
    Args:
        parsed_channel (str): Based on the provided context and instructions, which channel should we look at? 
            Channels typically start with / but not always.
            {{current_channel}}

    Returns:
        ChannelId: A ChannelId object containing channel and channel_url if found, None otherwise.
    """
    return get_channel_id(parsed_channel)

  def get_user_id(self, user: str) -> UserId:
    """
    Get the parameters fid and username for user related tools.
    Use get_user_id when you need to fetch user related data.
    
    Args:
        user (str): Which user should we target?
            Users typically start with @, but not always.
            If the request is about self or uses a pronoun, study the context and instructions carefully to figure out the intended user.
        
    Returns:
        UserId: A UserId object containing a valid user fid and username, None otherwise.
    """
    return get_user_id(user)
  
  def get_random_user_in_channel(self, channel_id: ChannelId) -> UserId:
    """
    Get the parameters fid and username for user related tools when you need to select a random user from a specific channel.
    
    Args:
        channel_id (ChannelId): The channel to fetch a random active user.
        
    Returns:
        UserId: A UserId object containing a valid user fid and username, None otherwise.
    """
    return get_random_user_in_channel(self.state.bot_id, channel_id)
  
  def get_random_user_in_general(self) -> UserId:
    """
    Get the parameters fid and username for user related tools when you need to select a random user from the general feed.
        
    Returns:
        UserId: A UserId object containing a valid user fid and username, None otherwise.
    """
    return get_random_user_in_general(self.state.bot_id)
  
  def get_user_info(self, user_id: UserId) -> UserInfo:
    """
    Get basic information for a user
    
    Args:
        user_id (UserId): The user identifier parameters.
        
    Returns:
        UserInfo: A UserInfo object containing the user's basic information, None otherwise.
    """
    return get_user_info(user_id.username)
  
  def get_news(self, search_phrase: SearchPhrase) -> News:
    """
    Get a news story
    
    Args:
        search_phrase (SearchPhrase): search phrase to pull recent news.
        
    Returns:
        News: A News object containing the news story, None otherwise.
    """
    return get_news(search_phrase.search)
  
  def get_favorite_users(self, user_id: UserId) -> FavoriteUsers:
    """
    Get the favorite accounts of a user.
    
    Args:
        user_id (UserId): The target user identifier.
        
    Returns:
        FavoriteUsers: A FavoriteUsers object containing the favorite accounts of a user, None otherwise.
    """
    return get_favorite_users(user_id.fid)
  
  def get_most_active_users(self, channel_id: ChannelId) -> MostActiveUsers:
    """
    Get the most active users in a channel.
    
    Args:
        channel_id (ChannelId): The channel to fetch the most active users from.
        
    Returns:
        MostActiveUsers: A MostActiveUsers object containing a data frame with most active user activity, None otherwise.
    """
    return get_most_active_users(channel_id)
  
  def get_casts_channel(self, channel_id: ChannelId) -> Casts:
    """
    Get the casts in a channel.
    
    Args:
        channel_id (ChannelId): The channel to fetch the casts from.
        
    Returns:
        Casts: The list of channel casts, or None if empty.
    """
    return get_casts_channel(channel_id)
  
  def get_casts_keyword(self, keyword: Keyword) -> Casts:
    """
    Fetch casts with a keyword.
    Use get_casts_keyword when you want to use a single keyword.
    but if you need to search for a phrase with multiple words, use get_casts_search instead.
    
    Args:
        keyword (Keyword): The keyword to fetch the casts from.
        
    Returns:
        Casts: The list of matching casts, or None if empty.
    """
    return get_casts_keyword(keyword)
  
  def get_casts_search(self, search_phrase: SearchPhrase) -> Casts:
    """
    Fetch casts with a search phrase.
    Use get_casts_search when you want to use a multiple word search phrase.
    but if you need to search for a single keyword, use get_casts_keyword instead.  
    
    Args:
        search_phrase (SearchPhrase): The search phrase to use for fetching casts.
        
    Returns:
        Casts: The list of matching casts, or None if empty.
    """
    return get_casts_search(search_phrase)
  
  def get_casts_user(self, user_id: UserId) -> Casts:
    """
    Fetch casts from a user.
    Use get_casts_user when you want to fetch casts from a specific user. 
    
    Args:
        user_id (UserId): The user identifier.
        
    Returns:
        Casts: The list of casts from the user, or None if empty.
    """
    return get_casts_user(user_id)
  
  def aggregate_casts(self, description: str, casts1: Casts, casts2: Casts) -> Casts:
    """
    Aggregate 2 lists of casts.
    Use aggregate_casts when you need to combine 2 lists of casts into one single collection.
    
    Args:
        description (str): The description of the new collection of casts.
        casts1: First list of casts.
        casts2: Second list of casts.
        
    Returns:
        Casts: The aggregated casts, or None if empty.
    """
    return aggregate_casts(description, [casts1, casts2])
  
  def get_bot_casts_in_channel(self, channel_id: ChannelId) -> Casts:
    """
    Get the casts posted by the bot (yourself) in a channel.
    
    Args:
        channel_id (ChannelId): The channel to fetch the casts from.
        
    Returns:
        Casts: The list of casts posted by the bot (yourself) in the selected channel, or None if empty.
    """
    return get_bot_casts_in_channel(self.state.bot_id, channel_id)
  
  def get_bot_casts_all(self) -> Casts:
    """
    Get all the casts posted by the bot (yourself).
    
    Returns:
        Casts: The list of all casts posted by the bot (yourself), or None if empty.  
    """
    return get_bot_casts_all(self.state.bot_id)
  
  def get_trending(self) -> Casts:
    """
    Get the globally trending casts.
    
    Returns:
        Casts: The list of trending casts, or None if empty.
    """
    return get_trending()
  
  def get_user_reactions(self, user_id: UserId) -> Reactions:
    """
    Get the reactions (likes, replies and recasts) of a user.
    
    Args:
        user_id (UserId): The user identifier.
        
    Returns:
        list[Reaction]: The list of reactions, or None if empty.
    """
    return get_user_reactions(user_id.fid)

  def make_cast_stats_sql_query(self) -> DuneQuery:
    """
    Make a SQL query to fetch cast statistics from Dune Analytics.
    Use to access the full table of cast features.
    
    Returns:
        DuneQuery: A DuneQuery object containing the SQL query, None otherwise.
    """
    context = format_state(self.state, intro=True, variables=True)
    return make_cast_stats_sql_query(context, self.state.bot_name)
  
  def make_user_stats_sql_query(self) -> DuneQuery:
    """
    Make a SQL query to fetch user statistics from Dune Analytics.
    Use to access the full table of user features.
    
    Returns:
        DuneQuery: A DuneQuery object containing the SQL query, None otherwise.
    """
    context = format_state(self.state, intro=True, variables=True)
    return make_user_stats_sql_query(context, self.state.bot_name)
  
  def execute_dune_query(self, query: DuneQuery) -> DataFrame:
    """
    Execute a Dune query and return a DataFrame.
    
    Args:
        query (DuneQuery): The Dune query to execute.

    Returns:
        DataFrame: A DataFrame object containing the results of the Dune query, None otherwise.
    """
    return execute_dune_query(query)
  
  def new_keyword(self, keyword: str) -> Keyword:
    """
    Instantiates a keyword object to be used for searching casts.
    Use get_keyword when you need to search for posts with a single keyword and you already know which keyword to use.
    If you don't know which keyword to use yet, use generate_keyword instead.
    Do not use an abbreviation for the keyword, it has to be at least 4 characters long.
    The keyword should be a single word, not a phrase.
    
    Args:
        keyword (str): One single keyword to search for.
        
    Returns:
        Keyword: A Keyword object containing a valid keyword, None otherwise.
    """
    return new_keyword(keyword)
  
  def new_search_phrase(self, search: str) -> SearchPhrase:
    """
    Instantiates a search phrase object to be used for searching casts, fetching news, or use more-like-this algorithm.
    Use get_search_phrase when you need a multiple word search phrase and you already know which search phrase to use.
    If you don't know which search phrase to use yet, use generate_search_phrase instead.
    
    Args:
        search (str): What should we search for?
        
    Returns:
        SearchPhrase: A SearchPhrase object containing a valid search phrase, None otherwise.
    """
    return new_search_phrase(search)

  def generate_search_phrase(self) -> SearchPhrase:
    """
    Generates a search phrase to be used for searching casts, fetching news, or use more-like-this algorithm.
    Use generate_search_phrase when you don't know which search phrase to use yet and prefer to generate the search phrase at execution time.
    If you don't need to wait for new data and already know which search phrase to use, use new_search_phrase instead.
    
    Returns:
        SearchPhrase: A SearchPhrase object containing a valid search phrase, None otherwise.
    """
    context = format_state(self.state, intro=True, variables=True)
    next_steps = str(self.state.todo)
    return generate_search_phrase(self.state.bot_name, context, next_steps)
