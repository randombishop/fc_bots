# LIST OF FUNCTIONS

* run_sql: runs a SQL query.
* pick_cast: picks a cast from a sample by channel or keywords.
* digest_casts: summarizes a sample of casts by channel or keywords.
* favorite_users: finds the favorite accounts of a user.
* most_active_users: lists the most active users by channel or keywords.

# FUNCTIONS DETAILS

## run_sql
*Description:*
runs a {sql} query
*Parameters:*
* sql, text, required. Only read-only queries. If the sql doesn't look like a read-only query, return an error in the json object.

## pick_cast
*Description:*
selects top post from {channel} over last {num_days} days by {criteria}
*Parameters:*
* channel is an optional parameter and defaults to null
* num_days is an optional parameter and defaults to 1  
* criteria is free text and defaults to 'most interesting'

## digest_casts
*Description:*
Summarizes the last {num_days} casts/posts containing {keywords} from {channel}
*Parameters:*
* num_days, integer, optional, defaults to 1  
* keywords, comma separated list of keywords, optional, defaults to null
* channel, string, optional, defaults to null

## favorite_users
*Description:*
Who are the favorite users of {user}
*Parameters:*
* user, text or integer, required.

## most_active_users
*Description:*
Lists the most active users in channel {channel} over the last {num_days} days
*Parameters:*
* channel, text, required.
* num_days, integer, optional, defaults to 1