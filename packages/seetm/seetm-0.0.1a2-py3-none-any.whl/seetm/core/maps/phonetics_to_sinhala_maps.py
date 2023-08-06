# Vowel Keys and Maps
SI_VOWEL_KEYS = [
    'uu', 'oo', 'oe', 'aa', 'AA', 'Aa', 'ae', 'ii', 'ie', 'ee', 'ea', 'ei', 'uu', 'au',
    'O', 'a', 'A', 'i', 'e', 'u', 'o', 'E', 'I'
]
SI_VOWEL_PURE_MAP = {
    'uu': 'ඌ', 'oo': 'ඕ', 'oe': 'ඕ', 'aa': 'ආ', 'AA': 'ඈ', 'Aa': 'ඈ', 'ae': 'ඈ', 'ii': 'ඊ', 'ie': 'ඊ',
    'ee': 'ඒ', 'ea': 'ඒ', 'ei': 'ඒ', 'au': 'ඖ', 'O': 'ඖ', 'a': 'අ', 'A': 'ඇ', 'i': 'ඉ', 'e': 'එ', 'u': 'උ',
    'o': 'ඔ', 'E': 'ඓ', 'I': 'ඓ'
}
SI_VOWEL_SUFFIX_MAP = {
    'uu': 'ූ', 'oo': 'ෝ', 'oe': 'ෝ', 'aa': 'ා', 'AA': 'ෑ', 'Aa': 'ෑ', 'ae': 'ෑ', 'ii': 'ී', 'ie': 'ී',
    'ee': 'ේ', 'ea': 'ේ', 'ei': 'ේ', 'au': 'ෞ', 'O': 'ෞ', 'a': '', 'A': 'ැ', 'i': 'ි', 'e': 'ෙ', 'u': 'ු',
    'o': 'ො', 'E': 'ෛ', 'I': 'ෛ'
}

# Non-joining Character Keys and Maps [ + '\u200D']
SI_NON_JOINING_KEYS = [
    '\\r', 'x', 'H', 'R'
]
SI_NON_JOINING_MAP = {
    '\\r': 'ර්',
    'x': 'ං',
    'H': 'ඃ',
    'R': 'ඍ'
}

# Consonant Keys and Maps
SI_CONSONANT_KEYS = [
    'nndh', 'nnd', 'nng', 'mmb',
    'GN', 'KN', 'Lu', 'Th', 'Dh', 'gh', 'Ch', 'ph', 'kh', 'bh',
    'Sh', 'sh', 'dh', 'ch', 'th',
    'N', 'L', 'K', 'G', 'T', 'D', 'P', 'B', 'C', 'X', 'J',
    't', 'k', 'd', 'n', 'p', 'b', 'm', 'Y', 'y', 'j', 'l', 'v', 'w',
    's', 'h', 'f', 'g', 'c',
    'r'
]
SI_CONSONANT_MAP = {
    'nndh': 'ඳ', 'nnd': 'ඬ', 'nng': 'ඟ', 'mmb': 'ඹ',
    'GN': 'ඥ', 'KN': 'ඤ', 'Lu': 'ළු', 'Th': 'ථ', 'Dh': 'ධ', 'gh': 'ඝ', 'Ch': 'ඡ', 'ph': 'ඵ', 'kh': 'ඛ',
    'bh': 'භ', 'Sh': 'ෂ', 'sh': 'ශ', 'dh': 'ද', 'ch': 'ච', 'th': 'ත',
    'N': 'ණ', 'L': 'ළ', 'K': 'ඛ', 'G': 'ඝ', 'T': 'ඨ', 'D': 'ඪ', 'P': 'ඵ', 'B': 'භ', 'C': 'ඡ', 'X': 'ඞ',
    'J': 'ඣ', 't': 'ට', 'k': 'ක', 'd': 'ඩ', 'n': 'න', 'p': 'ප', 'b': 'බ', 'm': 'ම',
    'Y': 'ය', 'y': 'ය', 'j': 'ජ', 'l': 'ල', 'v': 'ව', 'w': 'ව',
    's': 'ස', 'h': 'හ', 'f': 'ෆ', 'g': 'ග', 'c': 'ච',
    'r': 'ර'
}

# Special Character Keys and Maps
SI_SPECIAL_KEYS = [
    'ruu',
    'ru'
]
SI_SPECIAL_MAP = {
    'ruu': 'ෲ',
    'ru': 'ෘ'
}