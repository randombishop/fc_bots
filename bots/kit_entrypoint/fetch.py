# Data interfaces
from bots.kit_interface.channel_id import ChannelId
from bots.kit_interface.keyword import Keyword
from bots.kit_interface.search_phrase import SearchPhrase
from bots.kit_interface.user_id import UserId
from bots.kit_interface.user_profile import UserProfile
from bots.kit_interface.news import News
from bots.kit_interface.favorite_users import FavoriteUsers
from bots.kit_interface.most_active_users import MostActiveUsers
from bots.kit_interface.casts import Casts
from bots.kit_interface.reaction import Reaction
# Tool implementations
from bots.kit_impl.fetch.get_channel_id import get_channel_id
from bots.kit_impl.fetch.get_keyword import get_keyword
from bots.kit_impl.fetch.get_search_phrase import get_search_phrase
from bots.kit_impl.fetch.get_user_id import get_user_id
from bots.kit_impl.fetch.get_random_user import get_random_user
from bots.kit_impl.fetch.get_user_profile import get_user_profile
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


class Fetch:
  
  def __init__(self, state):
    self.state = state

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
  
  def get_keyword(self, keyword: str) -> Keyword:
    """
    Create the keyword to be used for searching casts.
    Use get_keyword when you need to search for posts with a single keyword.
    Do not use an abbreviation for the keyword, it has to be at least 4 characters long.
    The keyword should be a single word, not a phrase.
    
    Args:
        keyword (str): One single keyword to search for.
        
    Returns:
        Keyword: A Keyword object containing a valid keyword, None otherwise.
    """
    return get_keyword(keyword)
  
  def get_search_phrase(self, search: str) -> SearchPhrase:
    """
    Create the search phrase to be used for searching casts, fetching news, or use more-like-this algorithm.
    Use get_search_phrase when you need a multiple word search phrase.
    
    Args:
        search (str): What should we search for?
        
    Returns:
        SearchPhrase: A SearchPhrase object containing a valid search phrase, None otherwise.
    """
    return get_search_phrase(search)

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
  
  def get_random_user(self, channel_id: ChannelId) -> UserId:
    """
    Get the parameters fid and username for user related tools when the instructions require selecting a random user.
    Use get_random_user when you need to fetch a random active user from a channel.
    
    Args:
        channel_id (ChannelId): The channel to fetch a random active user.
        
    Returns:
        UserId: A UserId object containing a valid user fid and username, None otherwise.
    """
    bot_id = self.state.get_bot_id()
    return get_random_user(bot_id,channel_id)
  
  def get_user_profile(self, user_id: UserId) -> UserProfile:
    """
    Get a user basic profile information
    
    Args:
        user_id (UserId): The user identifier parameters.
        
    Returns:
        UserProfile: A UserProfile object containing the user's basic profile information, None otherwise.
    """
    return get_user_profile(user_id.username)
  
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
  
  def aggregate_casts(self, description: str, cast_lists: list[Casts]) -> Casts:
    """
    Aggregate casts from multiple sources.
    Use aggregate_casts when you need to combine casts from multiple sources into one single collection.
    
    Args:
        description (str): The description of the new collection of casts.
        cast_lists (list[Casts]): The list of casts to aggregate.
        
    Returns:
        Casts: The aggregated casts, or None if empty.
    """
    return aggregate_casts(description, cast_lists)
  
  def get_bot_casts_in_channel(self, channel_id: ChannelId) -> Casts:
    """
    Get the casts posted by the bot (yourself) in a channel.
    
    Args:
        channel_id (ChannelId): The channel to fetch the casts from.
        
    Returns:
        Casts: The list of casts posted by the bot (yourself) in the selected channel, or None if empty.
    """
    return get_bot_casts_in_channel(self.state.get_bot_id(), channel_id)
  
  def get_bot_casts_all(self) -> Casts:
    """
    Get all the casts posted by the bot (yourself).
    
    Returns:
        Casts: The list of all casts posted by the bot (yourself), or None if empty.  
    """
    return get_bot_casts_all(self.state.get_bot_id())
  
  def get_trending(self) -> Casts:
    """
    Get the globally trending casts.
    
    Returns:
        Casts: The list of trending casts, or None if empty.
    """
    return get_trending()
  
  def get_user_reactions(self, user_id: UserId) -> list[Reaction]:
    """
    Get the reactions (likes, replies and recasts) of a user.
    
    Args:
        user_id (UserId): The user identifier.
        
    Returns:
        list[Reaction]: The list of reactions, or None if empty.
    """
    return get_user_reactions(user_id.fid)
