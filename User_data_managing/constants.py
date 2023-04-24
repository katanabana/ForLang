# during development change to 'Test_user_data'
PATH_TO_DATA_DIRECTORY = 'Test_user_data'
# characters in alphabets of different languages have different size in bytes
BYTES_PER_CHAR = {1: ('en', 'la', 'sw', 'haw'),
                  2: ('hr', 'eo', 'et', 'tl', 'haw', 'is', 'mg',
                      'sm', 'sn', 'sl', 'so', 'sw', 'tr', 'el', 'hy', 'iw', 'ar'),
                  3: ('ja', 'ko', 'zh-cn', 'zh-tw')}
# separators define where word start and ends in languages where there is word entity
# in other languages every character (usually hieroglyph) is considered as word entity
SEPARATORS = ' \t\n,.:;?!"\'(){}[]\\|/#№'
