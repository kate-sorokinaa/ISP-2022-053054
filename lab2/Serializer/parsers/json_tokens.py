LBRACE = "lbrace"
RBRACE = "rbrace"
LBRACKET = "lbracket"
RBRACKET = "rbracket"
NULL = "null"
STR = "str"
NUMBER = "number"
BOOL = "bool"
COLON = "colon"
COMMA = "comma"
EOF = "EOF"

TOKEN_REGEXPS = {
    LBRACE: r"{",
    RBRACE: r"}",
    LBRACKET: "\\[",
    RBRACKET: "\\]",
    NULL: r'null',
    STR: r'"[^"]*"',
    NUMBER: r'([0-9]*[.])?[0-9]+',
    BOOL: r'^(?:tru|fals)e',
    COLON: r":",
    COMMA: r",",
    EOF: "EOF"
}