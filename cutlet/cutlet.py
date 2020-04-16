import fugashi
import mojimoji
import jaconv
import re
import pathlib

from .mapping import *

SUTEGANA = 'ゃゅょぁぃぅぇぉ'
PUNCT = '\'".!?(),;:-'

systems = {
        'hepburn': HEPBURN,
        'kunrei': KUNREISHIKI,
        'nihon': NIHONSHIKI,
}

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
        self.system = system
        try:
            # make a copy so we can modify it
            self.table = dict(systems[system])
        except KeyError:
            print("unknown system: {}".format(system))
            raise

        self.tagger = fugashi.Tagger()
        self.exceptions = load_exceptions()

        self.use_tch = (self.system == 'hepburn')

    def add_exception(self, key, val):
        self.exceptions[key] = val

    def update_mapping(self, key, val):
        """Update mapping table.

        This can be used to mix common systems, or to modify particular details
        like how を should be romanized.
        """
        self.table[key] = val

    def slug(self, text):
        roma = self.romaji(text).lower()
        slug = re.sub(r'[^a-z0-9]+', '-', roma).strip('-')
        return slug

    def romaji(self, text):
        """Build a complete string from input text."""
        words = self.tagger.parseToNodeList(text)

        out = ''

        for wi, word in enumerate(words):
            pw = words[wi - 1] if wi > 0 else None
            nw = words[wi + 1] if wi < len(words) - 1 else None

            # resolve split verbs
            roma = self.romaji_word(word)
            if roma and out and out[-1] == 'っ':
                out = out[:-1] + roma[0]
            if word.feature.pos2 == '固有名詞':
                roma = roma.title()
            out += roma

            # no space sometimes
            # お酒 -> osake
            if word.feature.pos1 == '接頭辞': continue
            # 今日、 -> kyou, ; 図書館 -> toshokan
            if nw and nw.feature.pos1 in ('補助記号', '接尾辞'): continue
            # 思えば -> omoeba
            if nw and nw.feature.pos2 in ('接続助詞'): continue
            # 333 -> 333 ; this should probably be handled in mecab
            if (word.surface.isnumeric() and 
                    nw and nw.surface.isnumeric()):
                continue
            # そうでした -> sou deshita
            if (nw and word.feature.pos1 in ('動詞', '助動詞') and
                    nw and nw.feature.pos1 == '助動詞'):
                continue
            out += ' '
        # remove any leftover っ
        out = out.replace('っ', '')
        return out.strip()

    def romaji_word(self, word):
        """Word is a fugashi node, return a string"""

        if word.surface in self.exceptions:
            return self.exceptions[word.surface]

        if word.surface.isnumeric():
            return word.surface

        if word.surface.isascii():
            return word.surface

        if word.feature.pos1 == '補助記号':
            return self.table[word.surface]
        elif word.feature.pos1 == '助詞' and word.feature.pron == 'ワ':
            return 'wa'
        elif '-' not in word.surface and '-' in word.feature.lemma:
            # this is a foreign word with known spelling
            return word.feature.lemma.split('-')[-1]
        elif word.feature.kana:
            # for known words
            kana = jaconv.kata2hira(word.feature.kana)
            return self.map_kana(kana)
        else:
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

