#lexer_parser: Contiene archivos relacionados con el análisis léxico y sintáctico.
#tokens.py: Define clases o estructuras para representar los tokens.

import tokenize
from io import BytesIO

list_dict_variables=[]
list_procedures=[]

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

def search_list_dict(list_dict_variables,target):
    for dict in list_dict_variables:
        if str(target) in dict:
            return True
    return False

def parse_definition(tokens, index):

    if tokens[index].string in ['defVar', 'defProc']:#Definimos el procedimiento para verificar las definiciones de las funciones y las variables 
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------
        #PARSER VARIABLE DEFINITION
        if tokens[index].string == 'defVar':#Definimos la sintaxis y semantica para las definicion de las variables

            if tokens[index+1].type == tokenize.NAME:#la variable tiene que ser de tipo NAME no puede ser operador

                if tokens[index+2].type == tokenize.NAME and search_list_dict(list_dict_variables,tokens[index+2].string):#Si es una variable que es NAME entonces tienes que estar definida anteriormente
                                                           
                    list_dict_variables.append({str(tokens[index+1].string):tokens[index+2].string})
                    
                elif tokens[index+2].type == tokenize.NUMBER:#Si es numero 

                    list_dict_variables.append({str(tokens[index+1].string):tokens[index+2].string})
                    
                else:
                    
                    return False
            else:
                
                return False
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------
        #PARSER PROCEDURE DEFINITION
        elif tokens[index].string == 'defProc':#Definimos la sintaxis y semantica para la defincion de las funciones
            
            if tokens[index+1].type == tokenize.NAME:
                if tokens[index+2].string == "(" and tokens[index+3].string == ")":

                    list_procedures.append(tokens[index+1].string+" "+"()")
                else:
                    return False
                
            else:
                return False
    return True

#TokenInfo(type=63 (ENCODING), string='utf-8', start=(0, 0), end=(0, 0), line='')
def parse_execution(tokens):
    index = 1    
    while index < len(tokens)-1:
        if not parse_definition(tokens,index):
            return parse_definition(tokens,index)
        index+=1
    return True
        

tokens = tokenize_text_from_file("/home/keith/Downloads/LYM_PROY_0/sample_sample.txt")
#try:
#    print(parse_execution(tokens))
#except:
#    print("False")
print(parse_execution(tokens))
#parse_execution(tokens)

"""
parse_execution(tokens)
print(list_procedures)
"""



