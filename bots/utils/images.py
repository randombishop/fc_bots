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