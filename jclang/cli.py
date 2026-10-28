import sys
from pathlib import Path

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter

DEMO_FILE = Path(__file__).resolve().parent.parent / "examples" / "demo.jc"

class JcLang:
    def __init__(self):
        pass

    def main(self) -> None:
        print("Welcome to JcLang — the JSON and CSS inspired language!\n")
        print("Type 'demo' to run the demo file, or enter a file path.")
        print("Add '--verbose' to see detailed output.")
        print("Type 'q' to quit.\n")

        while True:
            user_input = input("Enter command: ").strip()
            if user_input.lower() == "q":
                print("Exiting JcLang. Goodbye!")
                break

            parts = user_input.split()
            if not parts:
                continue

            filename = None
            verbose = False

            if parts[0].lower() == "demo":
                filename = DEMO_FILE
                
            else:
                filename = parts[0]

            if "--verbose" in parts:
                verbose = True

            self.run_test_file(filename, verbose)

    def run_test_file(self, filename, verbose=False):
        try:
            with open(filename, "r") as file:
                source = file.read()
            self.run(source, verbose)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.\n")
        except Exception as e:
            print(f"An error occurred: {e}\n")

    def run(self, source, verbose=False):
        if verbose:
            print("\n" + "=" * 40)
            print("SOURCE CODE")
            print("=" * 40)
            print(source)

        scanner = Lexer(source)
        scanner.scan_tokens()

        if verbose:
            print("\n" + "=" * 40)
            print("TOKENS")
            print("=" * 40)
            scanner.print_tokens()

        parser = Parser(scanner.tokens)
        listOfStatements = parser.parse()

        if verbose:
            print("\n" + "=" * 40)
            print("PARSED STATEMENTS")
            print("=" * 40)
            for statement in listOfStatements:
                print(statement)

        interpreter = Interpreter()
        if verbose:
            print("\n" + "=" * 40)
            print("INTERPRETED OUTPUT")
            print("=" * 40)
        interpreter.interpret(listOfStatements)
        if verbose:
            print("=" * 40 + "\n")


def main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv
    jc_lang = JcLang()

    if not args:
        jc_lang.main()
        return

    verbose = "--verbose" in args
    files = [arg for arg in args if arg != "--verbose"]
    filename = DEMO_FILE if not files or files[0] == "demo" else files[0]
    jc_lang.run_test_file(filename, verbose)


if __name__ == "__main__":
    main()
