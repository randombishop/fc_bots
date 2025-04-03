import pandas
from bots.data.assistants import get_bot_prompts, get_bot_channels


def get_next_prompt(bot_id):
    df_prompts = pandas.DataFrame(get_bot_prompts(bot_id))
    df_channels = pandas.DataFrame(get_bot_channels(bot_id))
    df = df_prompts[df_prompts['channel'] != '#Autopilot#']
    df_auto = df_prompts[df_prompts['channel'] == '#Autopilot#']
    if len(df_auto) > 0:
      df_auto = df_auto.merge(df_channels[['channel']], how='cross')
      df_auto.drop(columns=['channel_x'], inplace=True)
      df_auto.rename(columns={'channel_y': 'channel'}, inplace=True)
      df = pandas.concat([df, df_auto], ignore_index=True)
    print(df)