import uuid
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy
from bots.i_prepare_step import IPrepareStep
from bots.utils.gcs import upload_to_gcs


class GetWordcloud(IPrepareStep):
  
  def prepare(self):
    mask = self.state.wordcloud_mask
    colormap = ImageColorGenerator(mask)
    words = self.state.wordcloud_counts
    filename = str(uuid.uuid4())+'.png'
    wordcloud = WordCloud(mask=mask,
                          background_color='black',  
                          min_font_size=1,
                          contour_width=1,
                          contour_color=(64, 64, 64),
                          repeat=True).generate_from_frequencies(words)
    wordcloud.recolor(color_func=colormap)
    wordcloud.to_file(filename)
    upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
    #os.remove(filename)
    self.state.wordcloud_url = f"https://fc.datascience.art/bot/main_files/{filename}"
    log = "<GetWordcloud>"
    log += f"url: {self.state.wordcloud_url}"
    log += "</GetWordcloud>\n"
    self.state.log += log
