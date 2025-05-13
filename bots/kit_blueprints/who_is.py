WhoIs = [
  {
    'tool': 'fetch',
    'method': 'get_user_info',
    'var_params': {
      'user_id': 'selected_user'
    },
    'variable_name': 'user_info',
    'variable_description': 'User basic info'
  },
  {
    'tool': 'fetch',  
    'method': 'get_casts_user',
    'var_params': {
      'user_id': 'selected_user'
    },
    'variable_name': 'casts_user',
    'variable_description': 'Casts from the selected user'
  },
  {
    'tool': 'fetch',
    'method': 'get_user_reactions',
    'var_params': {
      'user_id': 'selected_user'
    },
    'variable_name': 'user_reactions',
    'variable_description': 'User replies and reactions'
  },
  {
    'tool': 'prepare',
    'method': 'describe_pfp',
    'var_params': {
      'user_info': 'user_info'
    },
    'variable_name': 'pfp_description',
    'variable_description': 'Description of the user profile picture'
  },
  {
    'tool': 'prepare',
    'method': 'describe_user_casts',
    'var_params': {
      'user_id': 'selected_user', 
      'user_info': 'user_info', 
      'casts': 'casts_user'
    }, 
    'variable_name': 'casts_description',
    'variable_description': 'Description of the user casts'
  },
  {
    'tool': 'prepare',
    'method': 'describe_user_reactions',
    'var_params': {
      'user_id': 'selected_user', 
      'user_info': 'user_info', 
      'reactions': 'user_reactions'
    }, 
    'variable_name': 'reactions_description',
    'variable_description': 'Description of the user reactions'
  },
  {
    'tool': 'prepare',
    'method': 'create_avatar',
    'var_params': {
      'user_id': 'selected_user', 
      'user_info': 'user_info', 
      'pfp_description': 'pfp_description',
      'casts_user': 'casts_user',
      'casts_description': 'casts_description',
      'reactions_description': 'reactions_description'
    }, 
    'variable_name': 'avatar',
    'variable_description': 'Created Avatar'
  }
]
