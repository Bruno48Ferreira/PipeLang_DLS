# PipeLang

**DSL interpretada para análise de dados declarativa**  
Trabalho prático — Teoria da Computação e Compiladores  
Fundação Hermínio Ometto (FHO)

---

## Visão Geral

PipeLang é uma linguagem de domínio específico (DSL) que permite a profissionais sem experiência em programação descrever, executar e exportar pipelines de análise de dados em sintaxe declarativa e próxima da linguagem natural.

```pipe
pipeline "Vendas Norte por Categoria"
  load "dados_vendas.csv"
  filter coluna="regiao" valor="Norte"
  group_by coluna="categoria" agregacao=soma
  plot tipo=bar eixo_x="categoria" eixo_y="vendas"
  export "resultado_norte.csv"
end
```

---

## Instalação

```bash
pip install -r requirements.txt
```

**Dependências:** `ply`, `pandas`, `matplotlib`

---

## Uso

```bash
# Executar um pipeline
python main.py examples/vendas_norte.pipe

# Especificar diretório de saída
python main.py examples/vendas_norte.pipe --output resultados/

# Exibir a AST antes da execução
python main.py examples/vendas_norte.pipe --ast
```

---

## Gramática (EBNF)

```ebnf
programa   ::= 'pipeline' STRING instrucoes 'end'
instrucoes ::= instrucao+
instrucao  ::= load | filter | group_by | plot | export

load     ::= 'load' STRING
filter   ::= 'filter' 'coluna=' STRING 'valor=' STRING
group_by ::= 'group_by' 'coluna=' STRING 'agregacao=' AGREGFUNC
plot     ::= 'plot' 'tipo=' PLOTTYPE 'eixo_x=' STRING 'eixo_y=' STRING
export   ::= 'export' STRING

AGREGFUNC ::= 'soma' | 'media' | 'contagem'
PLOTTYPE  ::= 'bar' | 'line' | 'scatter'
STRING    ::= '"' [a-zA-Z0-9_./ ]+ '"'
```

---

## Instruções da Linguagem

| Instrução  | Parâmetros                                      | Descrição                              |
|------------|--------------------------------------------------|----------------------------------------|
| `load`     | `"arquivo.csv"`                                  | Carrega um CSV como fonte de dados     |
| `filter`   | `coluna="col"` `valor="val"`                     | Filtra linhas por valor de coluna      |
| `group_by` | `coluna="col"` `agregacao=soma\|media\|contagem` | Agrega dados por coluna               |
| `plot`     | `tipo=bar\|line\|scatter` `eixo_x="c"` `eixo_y="c"` | Gera e salva um gráfico           |
| `export`   | `"saida.csv"`                                    | Exporta o DataFrame atual para CSV     |

Comentários: linhas começando com `#`

---

## Arquitetura

```
Código-fonte (.pipe)
        |
   [Lexer - PLY/lex]          — Tokenização via AFDs
        |
   [Parser - PLY/yacc]        — LALR(1), gera AST
        |
   [Analisador Semântico]     — Valida tipos, argumentos, ordem
        |
   [Interpretador AST]        — Execução via Pandas + Matplotlib
        |
   Gráfico (.png) / CSV (.csv)
```

---

## Estrutura do Projeto

```
pipelang/
├── src/
│   ├── ast_nodes.py    # Nós da AST
│   ├── lexer.py        # Analisador léxico (PLY/lex)
│   ├── parser.py       # Analisador sintático (PLY/yacc, LALR(1))
│   ├── semantic.py     # Analisador semântico
│   └── interpreter.py  # Interpretador via caminhamento de AST
├── examples/
│   ├── dados_vendas.csv                     # 300 linhas × 11 colunas
│   ├── vendas_norte.pipe                    # soma por categoria
│   ├── eletronicos_geral.pipe               # média por região
│   ├── desempenho_vendedores.pipe           # soma por vendedor (Online)
│   ├── quantidade_por_produto.pipe          # média de unidades por produto
│   └── contagem_por_estado.pipe             # contagem por estado
|
├── colab/
│   ├── pipelang_colab.ipynb                 
│
├── main.py
```

---
## Autores

- Bruno Ferreira de Lima — 112389
- Marina de Souza Pina Oliveira — 111838
