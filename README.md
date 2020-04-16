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
- hyphenated words (the rules for this seem too irregular to automate)
- Traditional Hepburn in general is not supported

Internally, cutlet uses [fugashi](https://github.com/polm/fugashi), so you can
use the same dictionary you use for normal tokenization.

## Usage

    import cutlet
    katsu = cutlet.Cutlet()
    katsu.romaji("カツカレーは美味しい")
    # => 'cutlet curry wa oishii'

    # you can print a slug suitable for urls
    katsu.slug("カツカレーは美味しい")
    # => 'cutlet-curry-wa-oishii'

    # kunreisiki, nihonsiki work too
    katu = cutlet.Cutlet('kunrei')
    katu.romaji("富士見坂")
    # => 'Huzimi saka'

    # comparison
    nkatu = cutlet.Cutlet('nihon')

    sent = "彼女は王への手紙を読み上げた。"
    katsu.romaji(sent).capitalize()
    # => 'Kanojo wa ou e no tegami wo yomiageta.'
    katu.romaji(sent).capitalize()
    # => 'Kanozyo wa ou e no tegami o yomiageta.'
    nkatu.romaji(sent).capitalize()
    # => 'Kanozyo ha ou he no tegami wo yomiageta.'

## Alternatives

- [pykakasi](https://github.com/miurahr/pykakasi): self contained, it does segmentation on its own and uses its own dictionary.

