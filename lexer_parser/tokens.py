#lexer_parser: Contiene archivos relacionados con el análisis léxico y sintáctico.
#tokens.py: Define clases o estructuras para representar los tokens.
from tokenize import tokenize
from io import BytesIO

import tokenize
from io import BytesIO

def tokenize_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    token_generator = tokenize.tokenize(BytesIO(text.encode('utf-8')).readline)
    filtered_token_generator=[]

    filters=[tokenize.NEWLINE ,tokenize.INDENT , tokenize.DEDENT , tokenize.NL]#Borra las indentaciones, saltos de linea, espacios, etc. 
    for token in token_generator:
        if token.type not in filters:
            filtered_token_generator.append(token)    
    return filtered_token_generator
    #return list(token_generator)


def parse_definition(tokens, index):


    #if index >= len(tokens):
    #    return None, index
    
    if tokens[index].string in ['defVar', 'defProc']:#Definimos el procedimiento para verificar las definiciones de las funciones y las variables 

        if tokens[index].string == 'defVar':#Definimos la sintaxis y semntaica para las funciones 

            if tokens[index+1].type == tokenize.NAME:#la variable tiene que ser de tipo NAME no puede ser operador

                list_variables.append(tokens[index+1].string)

                if tokens[index+2].type == tokenize.NAME and tokens[index+2].string in list_variables:#Si es una variable que es NAME entonces tienes que estar definida anteriormente
                                                           
                    list_dict_variables.append({"key":tokens[index+1],"value":tokens[index+2].string})
                    
                
                elif tokens[index+2].type == tokenize.NUMBER:#Si es numero 

                    list_dict_variables.append({"key":tokens[index+1],"value":tokens[index+2].string})
                    
                else:
                    return False
            else:
                print("hola")  
                return False
    return "prueba"
        

#TokenInfo(type=63 (ENCODING), string='utf-8', start=(0, 0), end=(0, 0), line='')
def parse_execution(tokens):
    index = 1
    program=[]
    
    while index < len(tokens)-1:
        if not parse_definition(tokens,index):
            return parse_definition(tokens,index)
        index+=1
    return True
        

file_path = 'codigo.txt'
list_variables=[]
list_dict_variables=[]

tokens = tokenize_text_from_file("/home/keith/Downloads/LYM_PROY_0/sample_sample.txt")
print(parse_execution(tokens))
#parse_execution(tokens)




