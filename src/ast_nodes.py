"""Nós da Árvore Sintática Abstrata (AST)"""


class ProgramNode:
    def __init__(self, name: str, instructions: list):
        self.name = name
        self.instructions = instructions

    def __repr__(self):
        return f"ProgramNode(name={self.name!r}, instructions={self.instructions})"


class LoadNode:
    def __init__(self, filename: str):
        self.filename = filename

    def __repr__(self):
        return f"LoadNode(filename={self.filename!r})"


class FilterNode:
    def __init__(self, coluna: str, valor: str):
        self.coluna = coluna
        self.valor = valor

    def __repr__(self):
        return f"FilterNode(coluna={self.coluna!r}, valor={self.valor!r})"


class GroupByNode:
    def __init__(self, coluna: str, agregacao: str):
        self.coluna = coluna
        self.agregacao = agregacao

    def __repr__(self):
        return f"GroupByNode(coluna={self.coluna!r}, agregacao={self.agregacao!r})"


class PlotNode:
    def __init__(self, tipo: str, eixo_x: str, eixo_y: str):
        self.tipo = tipo
        self.eixo_x = eixo_x
        self.eixo_y = eixo_y

    def __repr__(self):
        return f"PlotNode(tipo={self.tipo!r}, eixo_x={self.eixo_x!r}, eixo_y={self.eixo_y!r})"


class ExportNode:
    def __init__(self, filename: str):
        self.filename = filename

    def __repr__(self):
        return f"ExportNode(filename={self.filename!r})"
