from langchain.agents import Tool
import uuid
import os
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy
from bots.utils.gcs import upload_to_gcs


def generate_wordcloud(input):
  state = input.state
  mask = numpy.array(state.wordcloud_mask)
  colormap = ImageColorGenerator(mask)
  words = state.wordcloud_counts
  filename1 = str(uuid.uuid4())+'.words.png'
  wordcloud = WordCloud(mask=mask,
                        background_color=None,  
                        min_font_size=1,
                        mode='RGBA',
                        repeat=True).generate_from_frequencies(words)
  wordcloud.recolor(color_func=colormap)
  wordcloud.to_file(filename1)
  wordcloud = Image.open(filename1).convert("RGBA")
  # Combine wordcloud with background
  filename2 = str(uuid.uuid4())+'.png'
  background = state.wordcloud_background
  background.paste(wordcloud, (0, 0), wordcloud)
  background.save(filename2)
  upload_to_gcs(local_file=filename2, target_folder='png', target_file=filename2)
  os.remove(filename1)
  os.remove(filename2)
  state.wordcloud_url = f"https://fc.datascience.art/bot/main_files/{filename2}"
  return {
    'wordcloud_url': state.wordcloud_url
  }

GenerateWordCloud = Tool(
  name="GenerateWordCloud",
  description="Generate the wordcloud image",
  func=generate_wordcloud
)