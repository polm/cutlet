HEPBURN = {
    # single characters
    "あ": "a",
    "い": "i",
    "う": "u",
    "え": "e",
    "お": "o",
    "か": "ka",
    "き": "ki",
    "く": "ku",
    "け": "ke",
    "こ": "ko",
    "が": "ga",
    "ぎ": "gi",
    "ぐ": "gu",
    "げ": "ge",
    "ご": "go",
    "さ": "sa",
    "し": "shi",
    "す": "su",
    "せ": "se",
    "そ": "so",
    "ざ": "za",
    "じ": "ji",
    "ず": "zu",
    "ぜ": "ze",
    "ぞ": "zo",
    "た": "ta",
    "ち": "chi",
    "つ": "tsu",
    "て": "te",
    "と": "to",
    "だ": "da",
    "ぢ": "zi",
    "づ": "zu",
    "で": "de",
    "ど": "do",
    "な": "na",
    "に": "ni",
    "ぬ": "nu",
    "ね": "ne",
    "の": "no",
    "は": "ha",
    "ひ": "hi",
    "ふ": "fu",
    "へ": "he",
    "ほ": "ho",
    "ば": "ba",
    "び": "bi",
    "ぶ": "bu",
    "べ": "be",
    "ぼ": "bo",
    "ぱ": "pa",
    "ぴ": "pi",
    "ぷ": "pu",
    "ぺ": "pe",
    "ぽ": "po",
    "ま": "ma",
    "み": "mi",
    "む": "mu",
    "め": "me",
    "も": "mo",
    "や": "ya",
    "ゆ": "yu",
    "よ": "yo",
    "ら": "ra",
    "り": "ri",
    "る": "ru",
    "れ": "re",
    "ろ": "ro",
    "わ": "wa",
    "ゐ": "yi",
    "う": "u",
    "ゑ": "ye",
    "を": "wo",
    "ん": "n",
    # obsolete / unusual
    "ゑ": "we",
    "ゐ": "wi",
    "ゔ": "vu",
    "ヸ": "vi",
    "ヷ": "va",
    "わ゙": "va",
    "ヹ": "ve",
    "ゑ゙": "ve",
    "ヺ": "vo",
    "を゙": "vo",
    # sutegana
    "ゃ": "ya",
    "ゅ": "yu",
    "ょ": "yo",
    "ぁ": "a",
    "ぃ": "i",
    "ぅ": "u",
    "ぇ": "e",
    "ぉ": "o",
    # unusual sutegana
    # These are mostly associated with Ainu or Taiwanese
    # https://ja.wikipedia.org/wiki/%E3%82%A2%E3%82%A4%E3%83%8C%E8%AA%9E%E4%BB%AE%E5%90%8D
    # https://ja.wikipedia.org/wiki/%E5%8F%B0%E6%B9%BE%E8%AA%9E%E4%BB%AE%E5%90%8D
    # These romaji are probably not very good, but are included to avoid errors.
    # Improvements are welcome.
    "ゕ": "ka",
    "ㇰ": "k",
    "ゖ": "ke",
    "ヶ": "ga",
    "こ": "ko",
    "ㇱ": "shi",
    "ㇲ": "su",
    "ㇳ": "to",
    "ㇴ": "nu",
    "ㇵ": "ha",
    "ㇶ": "hi",
    "ㇷ": "fu",
    "ㇸ": "he",
    "ㇹ": "ho",
    "ㇺ": "mu",
    "ㇻ": "ra",
    "ㇼ": "ri",
    "ㇽ": "ru",
    "ㇾ": "re",
    "ㇿ": "ro",
    "ゎ": "wa",
    "ㇷ゚": "p",
    # small kana extension
    "𛅐": "wi",
    "𛅑": "we",
    "𛅒": "wo",
    "𛅤": "wi",
    "𛅥": "we",
    "𛅦": "wo",
    "𛅧": "n",
    # digraphs
    "しゃ": "sha",
    "しゅ": "shu",
    "しょ": "sho",
    "じゃ": "ja",
    "じゅ": "ju",
    "じょ": "jo",
    "ちゃ": "cha",
    "ちゅ": "chu",
    "ちょ": "cho",
    # symbols
    "ー": "-",  # 長音符, only used when repeated
    "。": ".",
    "、": ",",
    "？": "?",
    "！": "!",
    "「": '"',
    "」": '"',
    "『": '"',
    "』": '"',
    "：": ":",
    "（": "(",
    "）": ")",
    "《": "(",
    "》": ")",
    "【": "[",
    "】": "]",
    "・": "/",
    "，": ",",
    # other
    "゚": "",  # combining handakuten by itself, just discard
    "゙": "",  # combining dakuten by itself
}

KUNREISHIKI = dict(HEPBURN)

KUNREISHIKI["し"] = "si"
KUNREISHIKI["じ"] = "zi"
KUNREISHIKI["つ"] = "tu"
KUNREISHIKI["ち"] = "ti"
KUNREISHIKI["しゃ"] = "sya"
KUNREISHIKI["しゅ"] = "syu"
KUNREISHIKI["しょ"] = "syo"
KUNREISHIKI["じゃ"] = "zya"
KUNREISHIKI["じゅ"] = "zyu"
KUNREISHIKI["じょ"] = "zyo"
KUNREISHIKI["ちゃ"] = "tya"
KUNREISHIKI["ちゅ"] = "tyu"
KUNREISHIKI["ちょ"] = "tyo"
KUNREISHIKI["ふ"] = "hu"

NIHONSHIKI = dict(KUNREISHIKI)
NIHONSHIKI["ぢ"] = "di"
NIHONSHIKI["づ"] = "du"

UNVOICED = "かきくけこさしすせそたちつてとはひふへほ"
VOICED = "がぎぐげござじずぜぞだぢづでどばびぶべぼ"


def add_dakuten(kk):
    """Given a kana (single-character string), add a dakuten."""
    try:
        ii = UNVOICED.index(kk)
        return VOICED[ii]
    except ValueError:
        # this is normal if the input is nonsense
        return None
