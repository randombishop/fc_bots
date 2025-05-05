WhoIs = [
  {
    'tool': 'fetch',
    'method': 'get_user_profile',
    'var_params': {
      'user_id': 'selected_user'
    },
    'variable_name': 'user_profile',
    'variable_description': 'User profile'
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
      'user_profile': 'user_profile'
    },
    'variable_name': 'pfp_description',
    'variable_description': 'Description of the user profile picture'
  },
  {
    'tool': 'prepare',
    'method': 'describe_user_casts',
    'var_params': {
      'user_id': 'selected_user', 
      'user_profile': 'user_profile', 
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
      'user_profile': 'user_profile', 
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
      'user_profile': 'user_profile', 
      'pfp_description': 'pfp_description',
      'casts_user': 'casts_user',
      'casts_description': 'casts_description',
    }, 
    'variable_name': 'avatar',
    'variable_description': 'Created Avatar'
  },
  {
    'tool': 'memorize',
    'method': 'memorize_user_profile',
    'var_params': {
      'user_id': 'selected_user',
      'user_profile': 'user_profile',
      'pfp_description': 'pfp_description',
      'casts_description': 'casts_description',
      'reactions_description': 'reactions_description',
      'avatar': 'avatar'
    }
  }
]
