import uuid
import os
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy
from bots.utils.gcs import upload_to_gcs
from bots.kit_interface.word_cloud_data import WordCloudData
from bots.kit_interface.word_cloud_mask import WordCloudMask
from bots.kit_interface.word_cloud_image import WordCloudImage


def create_wordcloud(data: WordCloudData, mask: WordCloudMask) -> WordCloudImage:
  mask_array = numpy.array(mask.mask)
  colormap = ImageColorGenerator(mask_array)
  words = data.word_counts
  filename1 = str(uuid.uuid4())+'.words.png'
  wordcloud = WordCloud(mask=mask_array,
                        background_color=None,  
                        min_font_size=1,
                        mode='RGBA',
                        repeat=True).generate_from_frequencies(words)
  wordcloud.recolor(color_func=colormap)
  wordcloud.to_file(filename1)
  wordcloud = Image.open(filename1).convert("RGBA")
  # Combine wordcloud with background
  filename2 = str(uuid.uuid4())+'.png'
  background = mask.background
  background.paste(wordcloud, (0, 0), wordcloud)
  background.save(filename2)
  upload_to_gcs(local_file=filename2, target_folder='png', target_file=filename2)
  os.remove(filename1)
  os.remove(filename2)
  wordcloud_url = f"https://fc.datascience.art/bot/main_files/{filename2}"
  return WordCloudImage(wordcloud_url)
