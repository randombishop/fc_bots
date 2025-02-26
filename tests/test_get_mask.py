from dotenv import load_dotenv
load_dotenv()
import unittest
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy
from bots.utils.tests import make_state
from bots.prepare.get_mask import GetMask
from bots.prepare.get_wordcloud import GetWordcloud

class TestGetMask(unittest.TestCase):
  
  def test1(self):
    wordcloud_text = "Japan posts: from zen cushions to Valentine's Day traditions, and even a lost mask!  Explore the diverse experiences of Farcaster users in Japan."
    wordcloud_counts = {'farcaster': 21, 'collection': 16, 'minted': 15, 'faces': 15, 'custom': 15, 'onchain': 15, 'exclusively': 15, 'farcasters': 15, 'gidi': 11, 'kong': 11, 'love': 5, 'fiery': 5, 'different': 5, 'look': 4, 'completed': 4, 'liveart': 4, 'dreamverse': 4, 'layer': 4, 'adventure': 4, 'dark': 3, 'days': 3, 'find': 3, 'peace': 3, 'beauty': 3, 'hand': 3, 'explore': 3, 'digital': 3, 'mysticism': 3, 'being': 3, 'creative': 3, 'vinci': 3, 'eternal': 3, 'vibes': 2, 'world': 2, 'time': 2, 'night': 2, 'itap': 2, 'denver': 2, 'dive': 2, 'everything': 2, 'cool': 2, 'style': 2, 'blending': 2, 'illustrations': 2, 'mona': 2, 'lisa': 2, 'leonardo': 2, 'painting': 2, 'every': 2, 'shes': 2, 'people': 2, 'opening': 2}
    
    state = make_state()
    state.wordcloud_text = wordcloud_text
    state.wordcloud_counts = wordcloud_counts
    state.wordcloud_mask = 'test8.mask.png'
    
    GetMask(state).prepare()
    #print(state.log)
    
    GetWordcloud(state).prepare()
    #mask = numpy.array(Image.open('test.mask.png'))  
    #wordcloud = WordCloud(mask=mask, background_color='black').generate_from_frequencies(wordcloud_counts)
    #plt.figure(figsize = (10, 10), facecolor = None) 
    #plt.imshow(wordcloud) 
    #plt.axis("off") 
    #plt.tight_layout(pad = 0) 
    #plt.savefig('test.wordcloud.png')
    #plt.close()
    