import fugashi
import jaconv
import mojimoji
import re
import pathlib
import sys

from .mapping import *

SUTEGANA = 'ゃゅょぁぃぅぇぉ'
PUNCT = '\'".!?(),;:-'

SYSTEMS = {
        'hepburn': HEPBURN,
        'kunrei': KUNREISHIKI,
        'nihon': NIHONSHIKI,
}

if sys.version_info >= (3, 7):
    def is_ascii(s):
        return s.isascii()
else:
    def is_ascii(s):
        for c in s: 
            if c > '\x7f': 
                return False 
        return True 

def has_foreign_lemma(word):
    """Check if a word has a foreign lemma.

    This doesn't get its own field, the lemma field is overloaded. There are
    also cases where the lemma field is overloaded with non-foreign-lemma
    information."""

    if '-' in word.surface: 
        # TODO check if this is actually possible in vanilla unidic
        return False

    if not word.feature.lemma:
        # No lemma means no foreign lemma
        return False

    lemma = word.feature.lemma

    if not '-' in lemma:
        return False

    cand = lemma.split('-')[-1]
    # NOTE: some words have 外国 instead of a foreign spelling. ジル
    # (Jill?) is an example. Unclear why this is the case.
    # NOTE: There are other hyphenated lemmas, like 私-代名詞. 
    if is_ascii(cand):
        return True

def load_exceptions():
    cdir = pathlib.Path(__file__).parent.absolute()
    exceptions = {}
    for line in open(cdir / 'exceptions.tsv'):
        line = line.strip()
        # allow comments and blanks
        if line[0] == '#' or not line: continue
        key, val = line.split('\t')
        exceptions[key] = val
    return exceptions

class Cutlet:
    def __init__(self, system='hepburn'):
        # allow 'nippon' for 'nihon'
        if system == 'nippon': system = 'nihon'
        self.system = system
        try:
            # make a copy so we can modify it
            self.table = dict(SYSTEMS[system])
        except KeyError:
            print("unknown system: {}".format(system))
            raise

        self.tagger = fugashi.Tagger()
        self.exceptions = load_exceptions()

        self.use_tch = (self.system in ('hepburn',))
        self.use_wa  = (self.system in ('hepburn', 'kunrei'))
        self.use_he  = (self.system in ('nihon',))
        self.use_wo  = (self.system in ('hepburn', 'nihon'))

        self.use_foreign_spelling = True
        self.ensure_ascii = True

    def add_exception(self, key, val):
        self.exceptions[key] = val

    def update_mapping(self, key, val):
        """Update mapping table.

        This can be used to mix common systems, or to modify particular details.
        """
        self.table[key] = val

    def slug(self, text):
        roma = self.romaji(text).lower()
        slug = re.sub(r'[^a-z0-9]+', '-', roma).strip('-')
        return slug

    def romaji(self, text, capitalize=True):
        """Build a complete string from input text.

        If `capitalize` is True, then the first letter of the text will be
        capitalized. This is typically the desired behavior if the input is a
        complete sentence.
        """
        if not text:
            return ''

        # convert all full-width alphanum to half-width, since it can go out as-is
        text = mojimoji.zen_to_han(text, kana=False)
        # replace half-width katakana with full-width
        text = mojimoji.han_to_zen(text, digit=False, ascii=False)

        words = self.tagger(text)

        out = ''

        for wi, word in enumerate(words):
            pw = words[wi - 1] if wi > 0 else None
            nw = words[wi + 1] if wi < len(words) - 1 else None

            # resolve split verbs / adjectives
            roma = self.romaji_word(word)
            if roma and out and out[-1] == 'っ':
                out = out[:-1] + roma[0]
            if word.feature.pos2 == '固有名詞':
                roma = roma.title()
            # handle punctuation with atypical spacing
            if word.surface in '「『':
                out += ' ' + roma
                continue
            if roma in '([':
                out += ' ' + roma
                continue
            if roma == '/':
                out += '/'
                continue
            out += roma

            # no space sometimes
            # お酒 -> osake
            if word.feature.pos1 == '接頭辞': continue
            # 今日、 -> kyou, ; 図書館 -> toshokan
            if nw and nw.feature.pos1 in ('補助記号', '接尾辞'): continue
            # special case for half-width commas
            if nw and nw.surface == ',': continue
            # 思えば -> omoeba
            if nw and nw.feature.pos2 in ('接続助詞'): continue
            # 333 -> 333 ; this should probably be handled in mecab
            if (word.surface.isdigit() and 
                    nw and nw.surface.isdigit()):
                continue
            # そうでした -> sou deshita
            if (nw and word.feature.pos1 in ('動詞', '助動詞', '形容詞') 
                   and nw.feature.pos1 == '助動詞'):
                continue
            out += ' '
        # remove any leftover っ
        out = out.replace('っ', '').strip()
        # capitalize the first letter
        if capitalize and len(out) > 0:
            tmp = out[0].capitalize()
            if len(out) > 1:
                tmp += out[1:]
            out = tmp
        return out

    def romaji_word(self, word):
        """Word is a fugashi node, return a string"""

        if word.surface in self.exceptions:
            return self.exceptions[word.surface]

        if word.surface.isdigit():
            return word.surface

        if is_ascii(word.surface):
            return word.surface

        # deal with unks first
        if word.is_unk:
            # at this point is is presumably an unk
            # Check character type using the values defined in char.def. 
            # This is constant across unidic versions so far but not guaranteed.
            if word.char_type == 6 or word.char_type == 7: # hiragana/katakana
                kana = jaconv.kata2hira(word.surface)
                return self.map_kana(kana)

            # At this point this is an unknown word and not kana. Could be
            # unknown kanji, could be hangul, cyrillic, something else.
            # By default ensure ascii by replacing with ?, but allow pass-through.
            if self.ensure_ascii:
                out = '?' * len(word.surface)
                return out
            else:
                return word.surface

        if word.feature.pos1 == '補助記号':
            # If it's punctuation we don't recognize, just discard it
            return self.table.get(word.surface, '')
        elif (self.use_wa and 
                word.feature.pos1 == '助詞' and word.feature.pron == 'ワ'):
            return 'wa'
        elif (not self.use_he and 
                word.feature.pos1 == '助詞' and word.feature.pron == 'エ'):
            return 'e'
        elif (not self.use_wo and 
                word.feature.pos1 == '助詞' and word.feature.pron == 'オ'):
            return 'o'
        elif (self.use_foreign_spelling and 
                has_foreign_lemma(word)):
            # this is a foreign word with known spelling
            return word.feature.lemma.split('-')[-1]
        elif word.feature.kana:
            # for known words
            kana = jaconv.kata2hira(word.feature.kana)
            return self.map_kana(kana)
        else:
            # unclear when we would actually get here
            return word.surface

    def map_kana(self, kana):
        out = ''
        for ki, char in enumerate(kana):
            nk = kana[ki + 1] if ki < len(kana) - 1 else None
            pk = kana[ki - 1] if ki > 0 else None
            out += self.get_single_mapping(pk, char, nk)
        return out

    def get_single_mapping(self, pk, kk, nk):
        # handle digraphs
        if pk and (pk + kk) in self.table:
            return self.table[pk + kk]
        if nk and (kk + nk) in self.table:
            return ''

        if nk and nk in SUTEGANA:
            return self.table[kk][:-1] + self.table[nk]
        if kk in SUTEGANA:
            return ''

        if kk == 'ー': # 長音符
            if pk: return self.table[pk][-1]
            else: return '-'
        
        if kk == 'っ':
            if nk:
                if self.use_tch and nk == 'ち': return 't'
                elif nk in 'あいうえおっ': return '-'
                else: return self.table[nk][0] # first character
            else: 
                # seems like it should never happen, but 乗っ|た is two tokens
                # so leave this as is and pick it up at the word level
                return 'っ'

        if kk == 'ん':
            if nk and nk in 'あいうえおやゆよ': return "n'"
            else: return 'n'

        return self.table[kk]

