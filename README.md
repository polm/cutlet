[![Current PyPI packages](https://badge.fury.io/py/cutlet.svg)](https://pypi.org/project/cutlet/)

# cutlet

<img src="https://github.com/polm/cutlet/raw/master/cutlet.png" width=125 height=125 alt="cutlet by Irasutoya" />

Cutlet is a tool to convert Japanese to romaji. 

Default settings:

- hepburn consonants: ji, shi, chi, fu
- no n-to-m transformation: Shinbashi
- words with known foreign spellings use that: cutlet
- no macrons: ousama
- verbs are joined: ikimasu
- spaces before particles: hon wo yonda

Internally, cutlet uses [fugashi](https://github.com/polm/fugashi), so you can
use the same dictionary you use for normal tokenization.

## Alternatives

- [pykakasi](https://github.com/miurahr/pykakasi): self contained, it does segmentation on its own and uses its own dictionary.

