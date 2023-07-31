import fugashi
import jaconv
import mojimoji
import unicodedata
import re
import pathlib
import sys

from .mapping import *

SUTEGANA = 'ゃゅょぁぃぅぇぉ'
PUNCT = '\'".!?(),;:-'
ODORI = '々〃ゝゞヽゞ'

SYSTEMS = {
        'hepburn': HEPBURN,
        'kunrei': KUNREISHIKI,
        'nihon': NIHONSHIKI,
}

if sys.version_info >= (3, 7):
    def is_ascii(s):
        """Check if a given string is ASCII."""
        return s.isascii()
else:
    def is_ascii(s):
        """Check if a given string is ASCII."""
        # this version is for old Pythons
        for c in s:
            if c > '\x7f':
                return False
        return True

def has_foreign_lemma(word):
    """Check if a word (node) has a foreign lemma.

    In UniDic, these lemmas don't get their own field, instead the lemma field
    is overloaded. There are also cases where the lemma field is overloaded
    with non-foreign-lemma information.
    """

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
    # There are other hyphenated lemmas, like 私-代名詞.
    if is_ascii(cand):
        return True

def load_exceptions():
    """Load list of exceptions from included data file."""
    cdir = pathlib.Path(__file__).parent.absolute()
    exceptions = {}
    with open(cdir / 'exceptions.tsv', encoding='utf-8') as exceptions_file:
        for line in exceptions_file:
            line = line.strip()
            # allow comments and blanks
            if line[0] == '#' or not line: continue
            key, val = line.split('\t')
            exceptions[key] = val
    return exceptions

class Cutlet:
    def __init__(
            self,
            system = 'hepburn',
            use_foreign_spelling = True,
            ensure_ascii = True,
):
        """Create a Cutlet object, which holds configuration as well as
        tokenizer state.

        `system` is `hepburn` by default, and may also be `kunrei` or
        `nihon`. `nippon` is permitted as a synonym for `nihon`.

        If `use_foreign_spelling` is true, output will use the foreign spelling
        provided in a UniDic lemma when available. For example, "カツ" will
        become "cutlet" instead of "katsu".

        If `ensure_ascii` is true, any non-ASCII characters that can't be
        romanized will be replaced with `?`. If false, they will be passed
        through.

        Typical usage:

        ```python
        katsu = Cutlet()
        roma = katsu.romaji("カツカレーを食べた")
        # "Cutlet curry wo tabeta"
        ```
        """
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

        # these are too minor to be worth exposing as arguments
        self.use_tch = (self.system in ('hepburn',))
        self.use_wa  = (self.system in ('hepburn', 'kunrei'))
        self.use_he  = (self.system in ('nihon',))
        self.use_wo  = (self.system in ('hepburn', 'nihon'))

        self.use_foreign_spelling = use_foreign_spelling
        self.ensure_ascii = ensure_ascii

    def add_exception(self, key, val):
        """Add an exception to the internal list.

        An exception overrides a whole token, for example to replace "Toukyou"
        with "Tokyo". Note that it must match the tokenizer output and be a
        single token to work. To replace longer phrases, you'll need to use a
        different strategy, like string replacement.
        """
        self.exceptions[key] = val

    def update_mapping(self, key, val):
        """Update mapping table for a single kana.

        This can be used to mix common systems, or to modify particular
        details. For example, you can use `update_mapping("ぢ", "di")` to
        differentiate ぢ and じ in Hepburn.

        Example usage:

        ```
        cut = Cutlet()
        cut.romaji("お茶漬け") # Ochazuke
        cut.update_mapping("づ", "du")
        cut.romaji("お茶漬け") # Ochaduke
        ```
        """
        self.table[key] = val

    def slug(self, text):
        """Generate a URL-friendly slug.

        After converting the input to romaji using `Cutlet.romaji` and making
        the result lower-case, any runs of non alpha-numeric characters are
        replaced with a single hyphen. Any leading or trailing hyphens are
        stripped.
        """
        roma = self.romaji(text).lower()
        slug = re.sub(r'[^a-z0-9]+', '-', roma).strip('-')
        return slug

    def romaji(self, text, capitalize=True, title=False):
        """Build a complete string from input text.

        If `capitalize` is true, then the first letter of the text will be
        capitalized. This is typically the desired behavior if the input is a
        complete sentence.

        If `title` is true, then words will be capitalized as in a book title.
        This means most words will be capitalized, but some parts of speech
        (particles, endings) will not.
        """
        if not text:
            return ''

        # perform unicode normalization
        text = unicodedata.normalize('NFKC', text)
        # convert all full-width alphanum to half-width, since it can go out as-is
        text = mojimoji.zen_to_han(text, kana=False)
        # replace half-width katakana with full-width
        text = mojimoji.han_to_zen(text, digit=False, ascii=False)

        words = self.tagger(text)

        out = ''

        for wi, word in enumerate(words):
            pw = words[wi - 1] if wi > 0 else None
            nw = words[wi + 1] if wi < len(words) - 1 else None

            # handle possessive apostrophe as a special case
            if (word.surface == "'" and
                    (nw and nw.char_type == 5 and not nw.white_space) and
                    not word.white_space):
                # remove preceeding space
                out = out[:-1]
                out += word.surface
                continue

            # resolve split verbs / adjectives
            roma = self.romaji_word(word)
            if roma and out and out[-1] == 'っ':
                out = out[:-1] + roma[0]
            if word.feature.pos2 == '固有名詞':
                roma = roma.title()
            if (title and
                word.feature.pos1 not in ('助詞', '助動詞', '接尾辞') and
                not (pw and pw.feature.pos1 == '接頭辞')):
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
            if (nw and word.feature.pos1 in ('動詞', '助動詞','形容詞')
                   and nw.feature.pos1 == '助動詞'
                   and nw.surface != 'です'):
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
        """Return the romaji for a single word (node)."""

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
        """Given a list of kana, convert them to romaji.

        The exact romaji resulting from a kana sequence depend on the preceding
        or following kana, so this handles that conversion.
        """
        out = ''
        for ki, char in enumerate(kana):
            nk = kana[ki + 1] if ki < len(kana) - 1 else None
            pk = kana[ki - 1] if ki > 0 else None
            out += self.get_single_mapping(pk, char, nk)
        return out

    def get_single_mapping(self, pk, kk, nk):
        """Given a single kana and its neighbors, return the mapped romaji."""
        # handle odoriji
        # NOTE: This is very rarely useful at present because odoriji are not
        # left in readings for dictionary words, and we can't follow kana
        # across word boundaries.
        if kk in ODORI:
            if kk in 'ゝヽ':
                if pk: return pk
                else: return '' # invalid but be nice
            if kk in 'ゞヾ': # repeat with voicing
                if not pk: return ''
                vv = add_dakuten(pk)
                if vv: return self.table[vv]
                else: return ''
            # remaining are 々 for kanji and 〃 for symbols, but we can't
            # infer their span reliably (or handle rendaku)
            return ''


        # handle digraphs
        if pk and (pk + kk) in self.table:
            return self.table[pk + kk]
        if nk and (kk + nk) in self.table:
            return ''

        if nk and nk in SUTEGANA:
            if kk == 'っ': return '' # never valid, just ignore
            return self.table[kk][:-1] + self.table[nk]
        if kk in SUTEGANA:
            return ''

        if kk == 'ー': # 長音符
            if pk and pk in self.table: return self.table[pk][-1]
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
