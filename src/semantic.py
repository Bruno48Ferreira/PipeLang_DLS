"""Analisador semântico da PipeLang.
"""

from src.ast_nodes import (
    ProgramNode, LoadNode, FilterNode, GroupByNode, PlotNode, ExportNode
)

_VALID_PLOT_TYPES = {'bar', 'line', 'scatter'}
_VALID_AGG_FUNCS  = {'soma', 'media', 'contagem'}


class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    def analyze(self, program: ProgramNode) -> None:
        instructions = program.instructions

        if not instructions:
            raise SemanticError("O pipeline não contém nenhuma instrução.")

        if not isinstance(instructions[0], LoadNode):
            raise SemanticError(
                "A primeira instrução do pipeline deve ser 'load'."
            )

        load_seen = False
        for instr in instructions:
            if isinstance(instr, LoadNode):
                self._check_load(instr)
                load_seen = True
            elif isinstance(instr, FilterNode):
                self._check_filter(instr, load_seen)
            elif isinstance(instr, GroupByNode):
                self._check_group_by(instr, load_seen)
            elif isinstance(instr, PlotNode):
                self._check_plot(instr, load_seen)
            elif isinstance(instr, ExportNode):
                self._check_export(instr, load_seen)
                
    def _check_load(self, node: LoadNode):
        if not node.filename:
            raise SemanticError("'load' requer um nome de arquivo não vazio.")

    def _check_filter(self, node: FilterNode, load_seen: bool):
        if not load_seen:
            raise SemanticError("'filter' deve aparecer após 'load'.")
        if not node.coluna:
            raise SemanticError("'filter' requer o parâmetro 'coluna'.")
        if not node.valor:
            raise SemanticError("'filter' requer o parâmetro 'valor'.")

    def _check_group_by(self, node: GroupByNode, load_seen: bool):
        if not load_seen:
            raise SemanticError("'group_by' deve aparecer após 'load'.")
        if node.agregacao not in _VALID_AGG_FUNCS:
            raise SemanticError(
                f"Função de agregação inválida: '{node.agregacao}'. "
                f"Use: {', '.join(sorted(_VALID_AGG_FUNCS))}."
            )

    def _check_plot(self, node: PlotNode, load_seen: bool):
        if not load_seen:
            raise SemanticError("'plot' deve aparecer após 'load'.")
        if node.tipo not in _VALID_PLOT_TYPES:
            raise SemanticError(
                f"Tipo de gráfico inválido: '{node.tipo}'. "
                f"Use: {', '.join(sorted(_VALID_PLOT_TYPES))}."
            )
        if not node.eixo_x:
            raise SemanticError("'plot' requer o parâmetro 'eixo_x'.")
        if not node.eixo_y:
            raise SemanticError("'plot' requer o parâmetro 'eixo_y'.")

    def _check_export(self, node: ExportNode, load_seen: bool):
        if not load_seen:
            raise SemanticError("'export' deve aparecer após 'load'.")
        if not node.filename:
            raise SemanticError("'export' requer um nome de arquivo não vazio.")
