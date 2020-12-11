[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/polm/cutlet-demo/main/demo.py)
[![Current PyPI packages](https://badge.fury.io/py/cutlet.svg)](https://pypi.org/project/cutlet/)

# cutlet

<img src="https://github.com/polm/cutlet/raw/master/cutlet.png" width=125 height=125 alt="cutlet by Irasutoya" />

Cutlet is a tool to convert Japanese to romaji. Check out the [interactive demo][demo]!

[demo]: https://share.streamlit.io/polm/cutlet-demo/main/demo.py

**issueを英語で書く必要はありません。**

Features:

- support for [Modified Hepburn](https://en.wikipedia.org/wiki/Hepburn_romanization), [Kunreisiki](https://en.wikipedia.org/wiki/Kunrei-shiki_romanization), [Nihonsiki](https://en.wikipedia.org/wiki/Nihon-shiki_romanization) systems
- custom overrides for individual mappings
- custom overrides for specific words
- built in exceptions list (Tokyo, Osaka, etc.)
- uses foreign spelling when available in UniDic
- proper nouns are capitalized
- slug mode for url generation

Things not supported:

- traditional Hepburn n-to-m: Shimbashi
- macrons or circumflexes: Tōkyō, Tôkyô
- passport Hepburn: Satoh (but you can use an exception)
- hyphenating words
- Traditional Hepburn in general is not supported

Internally, cutlet uses [fugashi](https://github.com/polm/fugashi), so you can
use the same dictionary you use for normal tokenization.

## Installation

Cutlet can be installed through pip as usual.

    pip install cutlet

Note that if you don't have a MeCab dictionary installed you'll also have to
install one. If you're just getting started
[unidic-lite](https://github.com/polm/unidic-lite) is probably fine. 

    pip install unidic-lite

## Usage

A command-line script is included for quick testing. Just use `cutlet` and each
line of stdin will be treated as a sentence. You can specify the system to use
(`hepburn`, `kunrei`, `nippon`, or `nihon`) as the first argument.

    $ cutlet
    ローマ字変換プログラム作ってみた。
    Roma ji henkan program tsukutte mita.

In code:

```python
import cutlet
katsu = cutlet.Cutlet()
katsu.romaji("カツカレーは美味しい")
# => 'Cutlet curry wa oishii'

# you can print a slug suitable for urls
katsu.slug("カツカレーは美味しい")
# => 'cutlet-curry-wa-oishii'

# You can disable using foreign spelling too
katsu.use_foreign_spelling = False
katsu.romaji("カツカレーは美味しい")
# => 'Katsu karee wa oishii'

# kunreisiki, nihonsiki work too
katu = cutlet.Cutlet('kunrei')
katu.romaji("富士山")
# => 'Huzi yama'

# comparison
nkatu = cutlet.Cutlet('nihon')

sent = "彼女は王への手紙を読み上げた。"
katsu.romaji(sent)
# => 'Kanojo wa ou e no tegami wo yomiageta.'
katu.romaji(sent)
# => 'Kanozyo wa ou e no tegami o yomiageta.'
nkatu.romaji(sent)
# => 'Kanozyo ha ou he no tegami wo yomiageta.'
```

## Alternatives

- [kakasi](http://kakasi.namazu.org/index.html.ja): Historically important, but not updated since 2014. 
- [pykakasi](https://github.com/miurahr/pykakasi): self contained, it does segmentation on its own and uses its own dictionary.
- [kuroshiro](https://github.com/hexenq/kuroshiro): Javascript based.
- [kana](https://github.com/gojp/kana): Go based.

