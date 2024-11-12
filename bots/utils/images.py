import pandas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def table_image(df, filename, size=(4, 3), dpi=100):
  _, ax = plt.subplots(figsize=size)
  ax.axis('tight')
  ax.axis('off')
  table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
  table.auto_set_column_width(col=list(range(df.shape[1])))
  table.auto_set_font_size(False)
  table.set_fontsize(12)
  table.scale(2, 2)
  for i in range(len(df.columns)):
    table[0, i].set_facecolor('#40466e') 
    table[0, i].set_text_props(color='w')
  plt.savefig(filename, bbox_inches='tight', dpi=dpi)
  

def user_activity_chart(df, filename, size=(10, 6)):
  df = df.copy()
  del df['fid']
  del df['casts_total']
  df.set_index("User", inplace=True)
  plt.figure(figsize=size)
  dates = pandas.to_datetime(df.columns)
  for user in df.index:
    plt.plot(dates, df.loc[user], label=user)
  plt.title('Daily casts per user')
  plt.xlabel("Date")
  plt.ylabel("Number of Casts")
  plt.legend(title="Users", bbox_to_anchor=(1.05, 1))
  plt.grid(True)
  plt.xticks(rotation=45)
  plt.subplots_adjust(top=0.90, bottom=0.25, left=0.1, right=0.75) 
  plt.savefig(filename)
  
def make_wordcloud(words, filename):
  wordcloud = WordCloud(width = 800, height = 800).generate_from_frequencies(words)
  plt.figure(figsize = (5, 5), facecolor = None) 
  plt.imshow(wordcloud) 
  plt.axis("off") 
  plt.tight_layout(pad = 0) 
  plt.savefig(filename)