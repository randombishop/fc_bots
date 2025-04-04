import random


def format_bio(character, sample_size=5):
  bio = None
  if character is not None and character['bio'] is not None and len(character['bio']) > 0:
    bio = character['bio']
    if len(bio)>sample_size:
      bio = random.sample(bio, sample_size)
    random.shuffle(bio)
    bio = '\n'.join(bio)
  return bio


def format_lore(character, sample_size=5):
  lore = None
  if character is not None and character['lore'] is not None and len(character['lore']) > 0:
    lore = character['lore']
    if len(lore)>sample_size:
      lore = random.sample(lore, sample_size)
    random.shuffle(lore)
    lore = '\n'.join(lore)
  return lore