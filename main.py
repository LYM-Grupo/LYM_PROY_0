#main.py: Punto de entrada del programa. Lee el archivo de programa de muestra y llama a los módulos relevantes para analizarlo.
from lexer_parser import tokens as tok

tok.tokenizer("/home/keith/Downloads/LYM_PROY_0/sample_program.txt")