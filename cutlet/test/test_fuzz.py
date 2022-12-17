import pytest
from cutlet import Cutlet, normalize_text
from fugashi import Tagger
from hypothesis import given
from hypothesis.strategies import from_regex

# see here:
# https://stackoverflow.com/questions/19899554/unicode-range-for-japanese
HIRAGANA = "\u3041-\u3096"
KATAKANA = "\u30A0-\u30FF"
KANJI = "\u3400-\u3DB5\u4E00-\u9FCB\uF900-\uFA6A"
KATAKANA_HALF = "\uFF5F-\uFF9F"
MISC = "\u31F0-\u31FF\u3220-\u3243\u3280-\u337F"

JAREGEX = f"[{HIRAGANA}{KATAKANA}{KANJI}{KATAKANA_HALF}{MISC}]+"

@given(from_regex(JAREGEX))
def test_no_exception(ss):
    cutlet = Cutlet()
    cutlet.romaji(ss)


@given(from_regex(JAREGEX))
def test_node_count_match(ss):
    tagger = Tagger()
    cutlet = Cutlet()
    text = normalize_text(ss)
    nodes = tagger(text)
    tokens = cutlet.romaji_tokens(nodes)
    assert len(nodes) == len(tokens), "Number of output tokens doesn't match input"
