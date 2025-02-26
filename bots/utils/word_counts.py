import re
import unicodedata


ignore_words = {
  'able',
  'about',
  'above',
  'actually',
  'according',
  'after',
  'again',
  'against',
  'always',
  'almost',
  'also',
  'allow',
  'although',
  'arent',
  'back',
  'because',
  'been',
  'cant',
  'completely',
  'come',
  'could',
  'currently',
  'custom',
  'does',
  'doing',
  'dont',
  'done',
  'down',
  'even',
  'first',
  'find',
  'from',
  'getting',
  'going',
  'good',
  'have',
  'here',
  'into',
  'isnt',
  'just',
  'keep',
  'last',
  'lets',
  'like',
  'made',
  'make',
  'making',
  'many',
  'more',
  'most',
  'much',
  'need',
  'next',
  'once',
  'only',
  'other',
  'ours',
  'ourselves',
  'over',
  'really',
  'same',
  'should',
  'shouldnt',
  'since',
  'some',
  'someone',
  'something',
  'stay',
  'still',
  'such',
  'take',
  'than',
  'that',
  'their',
  'theirs',
  'them',
  'themselves',
  'then',
  'there',
  'these',
  'they',
  'think',
  'thing',
  'things',
  'this',
  'those',
  'through',
  'today',
  'under',
  'until',
  'very',
  'wait',
  'want',
  'wasnt',
  'well',
  'were',
  'werent',
  'what',
  'when',
  'where',
  'which',
  'while',
  'whom',
  'will',
  'with',
  'wont',
  'would',
  'your',
  'youre',
  'yours',
  'yourself',
  'yourselves'
}



def remove_urls(text):
  text_without_urls = re.sub(r'https?://[^\s]+', '', text)
  return text_without_urls.lower()


def clean_text(text):
  # Normalize the text to NFD (decomposed) form
  normalized_text = unicodedata.normalize('NFD', text)
  # Remove all characters that are not letters or spaces
  cleaned_text = re.sub(r'[^a-zA-Z\u00C0-\u017F ]+', '', normalized_text)
  # Convert the result to lowercase
  return cleaned_text.lower()


def parse_text(text, target):
  text = remove_urls(text)
  text = clean_text(text)
  words = text.split()
  for word in words:
    if len(word) > 3 and word not in ignore_words:
      target[word] = target.get(word, 0) + 1


def get_word_counts(array, top):
  ans = {}
  for s in array:
    if s is not None and isinstance(s, str) and len(s) > 0:
      parse_text(s, ans)
  ans = sorted(ans.items(), key=lambda item: item[1], reverse=True)
  ans = ans[:top]
  ans = dict(ans)
  return ans
