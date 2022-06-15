"""
"""

KEYS = (
    # numeric prefix
    "#", ":",

    # main row
    # initials
        "S-", "H-", "G-", "D-",
    # final
        # medial
        "Y-", "W-",
        # nucleus & coda
        "A-", "I-", 
        "N-", "O-",
    # functional
        "F-", "X-",

    # alt row
    # initials
        "-s", "-h", "-g", "-d",
    # final
        # medial
        "-y", "-w",
        # nucleus & coda
        "-a", "-i", 
        "-n", "-o",
    # functional
        "-f", "-x",
    
    # special keys
    "^", "_"
)

IMPLICIT_HYPHEN_KEYS = KEYS

SUFFIX_KEYS = ()

UNDO_STROKE_STENO = "^"

NUMBER_KEY = None

NUMBERS = {}

KEYMAPS = {
    # 'Keyboard': {
    #     "S-": "q", "H-": "w", "G-": "e", "D-": "r", "F-": "t", 
    #     "Y-": "v",

    #     "X-": "y", "A-": "u", "I-": "i", "N-": "o", "O-": "p", 
    #     "W-": "n", 

    #     "#" : "c", ":" : "m",
    #     "^" : "[", "_" : "'"
    # },
    'Gemini PR': {
        # numeric prefix
        "#": ('#1', '#2', '#3', '#4', '#5', '#6'),
        ":": ('#7', '#8', '#9', '#A', '#B', '#C'),

        "S-": "S1-", "H-": "T-", "G-": "P-", "D-": "H-", "F-": "*1", 
        "-s": "S2-", "-h": "K-", "-g": "W-", "-d": "R-", "-f": "*2", 
        "Y-": "A-", "-y": "O-",

        "X-": "*3", "A-": "-F", "I-": "-P", "N-": "-L", "O-": "-T", 
        "-x": "*4", "-a": "-R", "-i": "-B", "-n": "-G", "-o": "-S", 
        "-w": "-E", "W-": "-U", 

        "^" : "-D",
        "_" : "-Z", 
    }
}

ORTHOGRAPHY_RULES = []
ORTHOGRAPHY_RULES_ALIASES = {}
ORTHOGRAPHY_WORDLIST = None

DICTIONARIES_ROOT = '.'
DEFAULT_DICTIONARIES = ('overwrite.json', '10dpy_dict.py')
