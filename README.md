[![Current PyPI packages](https://badge.fury.io/py/cutlet.svg)](https://pypi.org/project/cutlet/)

# cutlet

<img src="https://github.com/polm/cutlet/raw/master/cutlet.png" width=125 height=125 alt="cutlet by Irasutoya" />

Cutlet is a tool to convert Japanese to romaji.

Features:

- support for [Modified Hepburn](https://en.wikipedia.org/wiki/Hepburn_romanization), [Kunreisiki](https://en.wikipedia.org/wiki/Kunrei-shiki_romanization), [Nihonsiki](https://en.wikipedia.org/wiki/Nihon-shiki_romanization) systems
- custom overrides for individual mappings
- custom overrides for specific words
- built in exceptions list (Tokyo, Osaka, etc.)
- uses foreign spelling when available in UniDic
- proper nouns are capitalized

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
    katu.romaji("富士見坂")
    # => 'Huzimi saka'

    # comparison
    nkatu = cutlet.Cutlet('nihon')

    sent = "彼女は王への手紙を読み上げた。"
    katsu.romaji(sent)
    # => 'Kanojo wa ou e no tegami wo yomiageta.'
    katu.romaji(sent)
    # => 'Kanozyo wa ou e no tegami o yomiageta.'
    nkatu.romaji(sent)
    # => 'Kanozyo ha ou he no tegami wo yomiageta.'

## Alternatives

- [pykakasi](https://github.com/miurahr/pykakasi): self contained, it does segmentation on its own and uses its own dictionary.

