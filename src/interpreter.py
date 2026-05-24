"""Interpretador AST da PipeLang."""

import os

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from src.ast_nodes import (
    ProgramNode, LoadNode, FilterNode, GroupByNode, PlotNode, ExportNode
)

_AGG_MAP = {'soma': 'sum', 'media': 'mean', 'contagem': 'count'}


class InterpreterError(Exception):
    pass


class Interpreter:
    def __init__(self, base_dir: str = ".", output_dir: str = "output"):
        self.base_dir = base_dir
        self.output_dir = output_dir
        self._df: pd.DataFrame | None = None
        self._pipeline_name: str = ""

    def execute(self, program: ProgramNode) -> dict:
        """Executa o pipeline e devolve um resumo dos artefatos gerados."""
        self._pipeline_name = program.name
        self._df = None
        artifacts: dict[str, list[str]] = {"graficos": [], "exportacoes": []}

        for instr in program.instructions:
            result = self._dispatch(instr)
            if result:
                kind, path = result
                artifacts[kind].append(path)

        return artifacts
    
    def _dispatch(self, node):
        dispatch = {
            LoadNode:    self._exec_load,
            FilterNode:  self._exec_filter,
            GroupByNode: self._exec_group_by,
            PlotNode:    self._exec_plot,
            ExportNode:  self._exec_export,
        }
        handler = dispatch.get(type(node))
        if handler is None:
            raise InterpreterError(f"Nó desconhecido: {type(node).__name__}")
        return handler(node)

    def _exec_load(self, node: LoadNode):
        path = self._resolve_path(node.filename)
        if not os.path.exists(path):
            raise InterpreterError(f"Arquivo não encontrado: '{path}'")
        try:
            self._df = pd.read_csv(path)
            print(f"  [load] '{path}' carregado — {len(self._df)} linhas, "
                  f"{len(self._df.columns)} colunas.")
        except Exception as exc:
            raise InterpreterError(f"Falha ao carregar '{path}': {exc}") from exc

    def _exec_filter(self, node: FilterNode):
        self._require_df("filter")
        col = node.coluna
        if col not in self._df.columns:
            raise InterpreterError(
                f"Coluna '{col}' não encontrada. "
                f"Disponíveis: {list(self._df.columns)}"
            )
        val = self._coerce(node.valor, self._df[col])
        before = len(self._df)
        self._df = self._df[self._df[col] == val].copy()
        print(f"  [filter] '{col}' == {val!r} => {len(self._df)}/{before} linhas mantidas.")

    def _exec_group_by(self, node: GroupByNode):
        self._require_df("group_by")
        col = node.coluna
        if col not in self._df.columns:
            raise InterpreterError(
                f"Coluna '{col}' não encontrada. "
                f"Disponíveis: {list(self._df.columns)}"
            )
        agg = _AGG_MAP[node.agregacao]
        numeric_cols = self._df.select_dtypes(include='number').columns.tolist()
        if not numeric_cols:
            raise InterpreterError(
                "Nenhuma coluna numérica encontrada para agregação."
            )
        self._df = (
            self._df.groupby(col)[numeric_cols]
            .agg(agg)
            .reset_index()
        )
        print(f"  [group_by] agrupado por '{col}' com '{node.agregacao}' "
              f"=> {len(self._df)} grupos.")

    def _exec_plot(self, node: PlotNode) -> tuple[str, str]:
        self._require_df("plot")
        x_col, y_col = node.eixo_x, node.eixo_y
        for col in (x_col, y_col):
            if col not in self._df.columns:
                raise InterpreterError(
                    f"Coluna '{col}' não encontrada para o gráfico. "
                    f"Disponíveis: {list(self._df.columns)}"
                )
        os.makedirs(self.output_dir, exist_ok=True)
        safe_name = self._pipeline_name.replace(" ", "_")
        filename = f"{safe_name}_{node.tipo}.png"
        filepath = os.path.join(self.output_dir, filename)

        fig, ax = plt.subplots(figsize=(10, 6))
        if node.tipo == 'bar':
            ax.bar(self._df[x_col].astype(str), self._df[y_col])
        elif node.tipo == 'line':
            ax.plot(self._df[x_col], self._df[y_col], marker='o')
        elif node.tipo == 'scatter':
            ax.scatter(self._df[x_col], self._df[y_col])

        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"{self._pipeline_name} — {node.tipo}")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        fig.savefig(filepath, dpi=150)
        plt.close(fig)
        print(f"  [plot] gráfico salvo em '{filepath}'.")
        return ("graficos", filepath)

    def _exec_export(self, node: ExportNode) -> tuple[str, str]:
        self._require_df("export")
        os.makedirs(self.output_dir, exist_ok=True)
        path = os.path.join(self.output_dir, node.filename)
        self._df.to_csv(path, index=False)
        print(f"  [export] '{path}' exportado — {len(self._df)} linhas.")
        return ("exportacoes", path)

    def _require_df(self, instrucao: str):
        if self._df is None:
            raise InterpreterError(
                f"'{instrucao}' chamado antes de 'load'."
            )

    def _resolve_path(self, filename: str) -> str:
        if os.path.isabs(filename):
            return filename
        return os.path.join(self.base_dir, filename)

    @staticmethod
    def _coerce(value: str, series: pd.Series):
        """Tenta converter o valor de filtro para o tipo da coluna."""
        if pd.api.types.is_numeric_dtype(series):
            try:
                f = float(value)
                return int(f) if f == int(f) else f
            except ValueError:
                pass
        return value
