import random


def format_bio(bio, sample_size=5):
  if len(bio)>sample_size:
    bio = random.sample(bio, sample_size)
  random.shuffle(bio)
  return '\n'.join(bio)


def format_lore(lore, sample_size=5):
  if len(lore)>sample_size:
    lore = random.sample(lore, sample_size)
  random.shuffle(lore)
  return '\n'.join(lore)