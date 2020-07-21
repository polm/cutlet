

HEPBURN = {
# single characters
'あ':'a',
'い':'i',
'う':'u',
'え':'e',
'お':'o',
'か':'ka',
'き':'ki',
'く':'ku',
'け':'ke',
'こ':'ko',
'が':'ga',
'ぎ':'gi',
'ぐ':'gu',
'げ':'ge',
'ご':'go',
'さ':'sa',
'し':'shi',
'す':'su',
'せ':'se',
'そ':'so',
'ざ':'za',
'じ':'ji',
'ず':'zu',
'ぜ':'ze',
'ぞ':'zo',
'た':'ta',
'ち':'chi',
'つ':'tsu',
'て':'te',
'と':'to',
'だ':'da',
'ぢ':'zi',
'づ':'zu',
'で':'de',
'ど':'do',
'な':'na',
'に':'ni',
'ぬ':'nu',
'ね':'ne',
'の':'no',
'は':'ha',
'ひ':'hi',
'ふ':'fu',
'へ':'he',
'ほ':'ho',
'ば':'ba',
'び':'bi',
'ぶ':'bu',
'べ':'be',
'ぼ':'bo',
'ぱ':'pa',
'ぴ':'pi',
'ぷ':'pu',
'ぺ':'pe',
'ぽ':'po',
'ま':'ma',
'み':'mi',
'む':'mu',
'め':'me',
'も':'mo',
'や':'ya',
'ゆ':'yu',
'よ':'yo',
'ら':'ra',
'り':'ri',
'る':'ru',
'れ':'re',
'ろ':'ro',
'わ':'wa',
'ゐ':'yi',
'う':'u',
'ゑ':'ye',
'を':'wo',
'ん':'n',

# obsolete / unusual
'ゑ':'we',
'ゐ':'wi',
'ゔ': 'vu',

# sutegana

'ゃ':'ya',
'ゅ':'yu',
'ょ':'yo',
'ぁ':'a',
'ぃ':'i',
'ぅ':'u',
'ぇ':'e',
'ぉ':'o',

# digraphs
'しゃ': 'sha',
'しゅ': 'shu',
'しょ': 'sho',
'じゃ': 'ja',
'じゅ': 'ju',
'じょ': 'jo',
'ちゃ': 'cha',
'ちゅ': 'chu',
'ちょ': 'cho',

# symbols
'。': '.',
'、': ',',
'？': '?',
'！': '!',
'「': '"',
'」': '"',
'『': '"',
'』': '"',
'：': ':',
'（': '(',
'）': ')',
'《': '(',
'》': ')',
'【': '[',
'】': ']',
'・': '/',
'，': ',',
}

KUNREISHIKI = dict(HEPBURN)

KUNREISHIKI['し'] = 'si'
KUNREISHIKI['じ'] = 'zi'
KUNREISHIKI['つ'] = 'tu'
KUNREISHIKI['ち'] = 'ti'
KUNREISHIKI['しゃ'] = 'sya'
KUNREISHIKI['しゅ'] = 'syu'
KUNREISHIKI['しょ'] = 'syo'
KUNREISHIKI['じゃ'] = 'zya'
KUNREISHIKI['じゅ'] = 'zyu'
KUNREISHIKI['じょ'] = 'zyo'
KUNREISHIKI['ちゃ'] = 'tya'
KUNREISHIKI['ちゅ'] = 'tyu'
KUNREISHIKI['ちょ'] = 'tyo'
KUNREISHIKI['ふ'] = 'hu'

NIHONSHIKI = dict(KUNREISHIKI)
NIHONSHIKI['ぢ'] = 'di'
NIHONSHIKI['づ'] = 'du'

