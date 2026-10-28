# JcLang

A small interpreted programming language with a syntax inspired by JSON and CSS, written in Python from scratch.

Built for TKO_7104 Programming Languages and Compilers course at University of Turku. It contains: a BNF grammar, a hand-written lexer, a recursive-descent parser that builds an AST and a tree-walking interpreter.

```
.function {
    name: sumTwoValues,
    parameters: {
        param: a,
        param: b
    },
    logic: {
        return: {
            value: a + b
        }
    }
}

.print {
    value: #sumTwoValues { a: 20, b: 20 }
}
```

## Getting started

You need Python 3.10 or newer. There are no third-party dependencies.

```sh
git clone https://github.com/espien/jc-lang.git
cd jc-lang

python -m jclang examples/demo.jc             # run a file
python -m jclang demo --verbose               # run the bundled demo and show every stage
python -m jclang                              # interactive prompt
```

The `--verbose` flag prints each stage of the pipeline: the raw source, the token stream, the parsed AST and finally the program output.

In interactive mode, enter a file path (or `demo`), optionally followed by `--verbose`. Enter `q` to quit.

## Language tour

Statements start with a `.directive` followed by a `{ key: value }` body. Comments start with `//`.

### Variables

```
.var { name: x, value: 2 + 3 * 4 }   // declaration
#x { value: x + 6 }                  // assignment
```

### Printing

```
.print { value: "Hello World!" }
.print { value: x }
```

### Conditionals

```
.if {
    condition: x < 20,
    logic: {
        .print { value: "less than 20" }
    },
    .else {
        logic: {
            .print { value: "20 or more" }
        }
    }
}
```

### Loops

```
.while {
    condition: x < 25,
    logic: {
        #x { value: x + 1 }
    }
}
```

### Functions

Functions are declared with `.function` and called with `#name { arg: value, ... }`:

```
.var { name: y, value: #sumTwoValues { a: 10, b: 5 } }
```

### Expressions

| Kind       | Operators / forms                         |
| ---------- | ----------------------------------------- |
| Equality   | `==`, `!=`                                |
| Comparison | `<`, `<=`, `>`, `>=`                      |
| Arithmetic | `+`, `-`, `*`, `/`                        |
| Unary      | `-`, `!`                                  |
| Literals   | numbers, `"strings"`, `true`/`false`, `null` |

Operator precedence follows the usual rules. `logic: { ... }` blocks introduce a new lexical scope.

The full grammar in BNF is in [`docs/grammar.bnf`](docs/grammar.bnf), and [`examples/demo.jc`](examples/demo.jc) shows every feature.

## How it works

```
source ──► Lexer ──► tokens ──► Parser ──► AST ──► Interpreter ──► output
```

| Stage       | File                                                     | Notes                                                                 |
| ----------- | -------------------------------------------------------- | --------------------------------------------------------------------- |
| Tokens      | [`tokens.py`](jclang/tokens.py)                          | Token types, keywords and directives                                  |
| Lexer       | [`lexer.py`](jclang/lexer.py)                            | Turns source text into tokens (operators, literals, keywords, identifiers, directives) |
| AST         | [`expressions.py`](jclang/expressions.py), [`statements.py`](jclang/statements.py) | Expression and statement node classes                  |
| Parser      | [`parser.py`](jclang/parser.py)                          | Top-down recursive-descent parser, one method per grammar rule        |
| Interpreter | [`interpreter.py`](jclang/interpreter.py)                | Walks the AST using the visitor pattern                               |
| Scopes      | [`environment.py`](jclang/environment.py)                | Nested environments for global and local variables                    |
| Functions   | [`callables.py`](jclang/callables.py), [`exceptions.py`](jclang/exceptions.py) | User-defined functions; `return` unwinds using an exception |
| CLI         | [`cli.py`](jclang/cli.py)                                | Command-line runner and interactive prompt                            |

## Project structure

```
jc-lang/
├── jclang/           # interpreter source (run with `python -m jclang`)
├── examples/
│   └── demo.jc       # demo program covering every feature
├── docs/
│   └── grammar.bnf   # language grammar in BNF
└── README.md
```
