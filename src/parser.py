"""Analisador sintático (parser)"""

import os
import ply.yacc as yacc

from src.lexer import tokens, build_lexer  # noqa: F401 — PLY exige 'tokens' no escopo
from src.ast_nodes import (
    ProgramNode, LoadNode, FilterNode, GroupByNode, PlotNode, ExportNode
)

def p_programa(p):
    'programa : PIPELINE STRING instrucoes END'
    p[0] = ProgramNode(name=p[2], instructions=p[3])

def p_instrucoes_multi(p):
    'instrucoes : instrucoes instrucao'
    p[0] = p[1] + [p[2]]

def p_instrucoes_single(p):
    'instrucoes : instrucao'
    p[0] = [p[1]]

def p_instrucao(p):
    '''instrucao : instr_load
                 | instr_filter
                 | instr_group_by
                 | instr_plot
                 | instr_export'''
    p[0] = p[1]

def p_load(p):
    'instr_load : LOAD STRING'
    p[0] = LoadNode(filename=p[2])

def p_filter(p):
    'instr_filter : FILTER COLUNA_EQ STRING VALOR_EQ STRING'
    p[0] = FilterNode(coluna=p[3], valor=p[5])

def p_group_by(p):
    'instr_group_by : GROUP_BY COLUNA_EQ STRING AGREGACAO_EQ agregfunc'
    p[0] = GroupByNode(coluna=p[3], agregacao=p[5])

def p_plot(p):
    'instr_plot : PLOT TIPO_EQ plottype EIXO_X_EQ STRING EIXO_Y_EQ STRING'
    p[0] = PlotNode(tipo=p[3], eixo_x=p[5], eixo_y=p[7])

def p_export(p):
    'instr_export : EXPORT STRING'
    p[0] = ExportNode(filename=p[2])

def p_agregfunc(p):
    '''agregfunc : SOMA
                 | MEDIA
                 | CONTAGEM'''
    p[0] = p[1]

def p_plottype(p):
    '''plottype : BAR
               | LINE
               | SCATTER'''
    p[0] = p[1]

def p_error(p):
    if p:
        raise SyntaxError(
            f"Linha {p.lineno}: erro de sintaxe próximo a '{p.value}'"
        )
    raise SyntaxError("Erro de sintaxe: fim de arquivo inesperado")

def build_parser(output_dir: str = "."):
    os.makedirs(output_dir, exist_ok=True)
    return yacc.yacc(outputdir=output_dir, debug=False, errorlog=yacc.NullLogger())


def parse(source: str, output_dir: str = ".") -> ProgramNode:
    lexer = build_lexer()
    parser = build_parser(output_dir=output_dir)
    result = parser.parse(source, lexer=lexer, tracking=True)
    return result
