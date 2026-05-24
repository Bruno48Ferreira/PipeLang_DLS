"""Ponto de entrada CLI da PipeLang.

Uso:
    python main.py <arquivo.pipe> [--output <dir>] [--ast]
"""

import argparse
import os
import sys

from src.lexer import LexicalError
from src.parser import parse
from src.semantic import SemanticAnalyzer, SemanticError
from src.interpreter import Interpreter, InterpreterError

_PARSER_CACHE = os.path.join(os.path.dirname(__file__), ".pipelang_cache")


def run(source_path: str, output_dir: str = "output", show_ast: bool = False):
    base_dir = os.path.dirname(os.path.abspath(source_path))

    with open(source_path, encoding="utf-8") as f:
        source = f.read()

    print(f"\nPipeLang — executando '{source_path}'")
    print("=" * 60)

    # 1. Análise léxica + sintática
    try:
        ast = parse(source, output_dir=_PARSER_CACHE)
    except LexicalError as exc:
        print(f"\n[ERRO LÉXICO] {exc}", file=sys.stderr)
        sys.exit(1)
    except SyntaxError as exc:
        print(f"\n[ERRO SINTÁTICO] {exc}", file=sys.stderr)
        sys.exit(1)

    if show_ast:
        print("\n--- AST ---")
        _print_ast(ast)
        print("-----------\n")

    # 2. Análise semântica
    try:
        SemanticAnalyzer().analyze(ast)
    except SemanticError as exc:
        print(f"\n[ERRO SEMÂNTICO] {exc}", file=sys.stderr)
        sys.exit(1)

    # 3. Interpretação
    try:
        interpreter = Interpreter(base_dir=base_dir, output_dir=output_dir)
        artifacts = interpreter.execute(ast)
    except InterpreterError as exc:
        print(f"\n[ERRO DE EXECUÇÃO] {exc}", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print(f"Pipeline '{ast.name}' concluído com sucesso.")
    if artifacts["graficos"]:
        print(f"  Gráficos: {artifacts['graficos']}")
    if artifacts["exportacoes"]:
        print(f"  Exportações: {artifacts['exportacoes']}")


def _print_ast(program):
    print(f"ProgramNode: '{program.name}'")
    for i, instr in enumerate(program.instructions, 1):
        print(f"  [{i}] {instr!r}")


def main():
    parser = argparse.ArgumentParser(
        description="Interpretador PipeLang — DSL para análise de dados"
    )
    parser.add_argument("arquivo", help="Arquivo .pipe a executar")
    parser.add_argument(
        "--output", default="output",
        help="Diretório de saída para gráficos e CSVs (padrão: output)"
    )
    parser.add_argument(
        "--ast", action="store_true",
        help="Exibe a AST antes da execução"
    )
    args = parser.parse_args()
    run(args.arquivo, output_dir=args.output, show_ast=args.ast)


if __name__ == "__main__":
    main()
