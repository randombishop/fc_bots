import matplotlib.pyplot as plt


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
  plt.figure(figsize=size)
  for user in df.index:
    plt.plot(df.columns, df.loc[user], label=user)
  plt.title('Daily casts per user')
  plt.xlabel("Date")
  plt.ylabel("Number of Casts")
  plt.legend(title="Users", bbox_to_anchor=(1.05, 1))
  plt.grid(True)
  plt.xticks(rotation=45)
  plt.subplots_adjust(top=0.90, bottom=0.25, left=0.1, right=0.9) 
  plt.savefig(filename)