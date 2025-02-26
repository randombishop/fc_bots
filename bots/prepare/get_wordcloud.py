import uuid
import os
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy
from bots.i_prepare_step import IPrepareStep
from bots.utils.gcs import upload_to_gcs


class GetWordcloud(IPrepareStep):
  
  def prepare(self):
    mask = numpy.array(self.state.wordcloud_mask)
    colormap = ImageColorGenerator(mask)
    words = self.state.wordcloud_counts
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
    background = self.state.wordcloud_background
    background.paste(wordcloud, (0, 0), wordcloud)
    background.save(filename2)
    upload_to_gcs(local_file=filename2, target_folder='png', target_file=filename2)
    os.remove(filename1)
    os.remove(filename2)
    self.state.wordcloud_url = f"https://fc.datascience.art/bot/main_files/{filename2}"
    log = "<GetWordcloud>"
    log += f"url: {self.state.wordcloud_url}"
    log += "</GetWordcloud>\n"
    self.state.log += log
