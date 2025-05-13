from PIL import Image


class WordCloudMask:
  """
  Mask used to render a word cloud.
  """
  
  def __init__(self, mask: Image.Image, background: Image.Image, width: int, height: int):
    self.mask = mask
    self.background = background
    self.width = width
    self.height = height
    
  def __str__(self) -> str:
    return f"{self.width}x{self.height} image"