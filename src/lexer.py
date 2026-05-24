"""Analisador léxico (lexer)"""

import ply.lex as lex

# Palavras reservadas da linguagem
_reserved = {
    'pipeline':  'PIPELINE',
    'end':       'END',
    'load':      'LOAD',
    'filter':    'FILTER',
    'group_by':  'GROUP_BY',
    'plot':      'PLOT',
    'export':    'EXPORT',
    'soma':      'SOMA',
    'media':     'MEDIA',
    'contagem':  'CONTAGEM',
    'bar':       'BAR',
    'line':      'LINE',
    'scatter':   'SCATTER',
}

tokens = (
    'PIPELINE', 'END', 'LOAD', 'FILTER', 'GROUP_BY', 'PLOT', 'EXPORT',
    'SOMA', 'MEDIA', 'CONTAGEM',
    'BAR', 'LINE', 'SCATTER',
    'COLUNA_EQ', 'VALOR_EQ', 'AGREGACAO_EQ', 'TIPO_EQ', 'EIXO_X_EQ', 'EIXO_Y_EQ',
    'STRING',
)

def t_EIXO_X_EQ(t):
    r'eixo_x='
    return t

def t_EIXO_Y_EQ(t):
    r'eixo_y='
    return t

def t_AGREGACAO_EQ(t):
    r'agregacao='
    return t

def t_COLUNA_EQ(t):
    r'coluna='
    return t

def t_VALOR_EQ(t):
    r'valor='
    return t

def t_TIPO_EQ(t):
    r'tipo='
    return t

def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]  # Remove aspas
    return t

def t_WORD(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = _reserved.get(t.value)
    if t.type is None:
        raise LexicalError(f"Linha {t.lineno}: identificador desconhecido '{t.value}'")
    return t

def t_COMMENT(t):
    r'\#[^\n]*'
    pass  # Ignora comentários de linha

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r'

def t_error(t):
    raise LexicalError(
        f"Linha {t.lineno}: caractere inválido '{t.value[0]}'"
    )


class LexicalError(Exception):
    pass


def build_lexer():
    return lex.lex()
