import unittest
from bots.utils.tests import make_bot


SMALL_DISTANCE = 0.25
def assert_expected_output(t, bot):
  t.assertEqual(bot.state.selected_action, 'MoreLikeThis')
  t.assertGreater(len(bot.state.casts), 0)
  top_result = bot.state.casts[0]
  t.assertLess(top_result['q_distance'], SMALL_DISTANCE)
  t.assertLess(top_result['dim_distance'], SMALL_DISTANCE)


class TestMoreLikeThis(unittest.TestCase):

  def test1(self):
    request = "More like this: Bitcoin is sweet!"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    
  def test2(self):
    parent_hash = '0x899f8e2fe0dd13241a336d7266273b1994476e86'
    request = "Find similar casts"
    bot = make_bot()
    bot.respond(request, parent_hash=parent_hash)
    bot.state.debug_action()
    assert_expected_output(self, bot)

  def test3(self):
    attachment_hash = '0x677a180098d6a0dca3fc1c4002ffc2889eca7fc9'
    request = "Other casts like this one?"
    bot = make_bot()
    bot.respond(request, attachment_hash=attachment_hash)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    
  def test4(self):
    # test with a deleted parent
    parent_hash = '0xb59fcfda9e859be648e5d5541d292a6fb8cc9fcb'
    request = "More like this"
    bot = make_bot()
    bot.respond(request, parent_hash=parent_hash)
    bot.state.debug_action()
    assert_expected_output(self, bot)
    