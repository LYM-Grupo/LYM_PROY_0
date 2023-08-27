#lexer_parser: Contiene archivos relacionados con el análisis léxico y sintáctico.
#tokens.py: Define clases o estructuras para representar los tokens.

def tokenizer(ruta_archivo):
    with open(ruta_archivo, "r") as file:
        for line in file:
            print(line.strip())
