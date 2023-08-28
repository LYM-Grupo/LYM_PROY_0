#lexer_parser: Contiene archivos relacionados con el análisis léxico y sintáctico.
#tokens.py: Define clases o estructuras para representar los tokens.

import tokenize
from io import BytesIO

list_dict_variables=[]
list_procedures=[]
list_built_function=[   
    {"key":"jump","args":2,"type_1":"value"},
    {"key":"walk_1","args":1,"type_1":"value"},
    {"key":"walk_2_D","args":2,"type_1":"value","type_2":"direction"},
    {"key":"walk_2_O","args":2,"type_1":"value","type_2":"orientation"}
]

direction=[]
orientation=[]

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

def extract_code_blocks(tokens):#Extrae bloque de codigo delimitados por {}
    code_blocks = []
    block = []
    depth = 0

    for token in tokens:
        if token.string == '{':
            depth += 1
            if depth == 1:
                block = []
        elif token.string == '}':
            depth -= 1
            if depth == 0:
                code_blocks.append(block)
        elif depth > 0:
            block.append(token)

    return code_blocks

def built_in_functions_analyzer(tokens):
    pass

def check_token_sequence(tokens):
    result = False 
    tokens=list(tokens)
    for i in range(0,len(tokens)-3):
        print(tokens[i].string)
        if tokens[i].type == tokenize.NAME:
            if tokens[i+1].type == tokenize.OP and tokens[i+1].string == ',':
                result = True
            else:
                return False
            
        elif tokens[i].type == tokenize.OP and tokens[i].string == ',':
            if tokens[i+1].type == tokenize.NAME:
                result = True
            else:
                return False
    return result

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
                if tokens[index+2].string == "(" and tokens[index].line[-1] == ")":

                    #list_procedures.append(tokens[index+1].string+" "+"()")
                    string_proc = tokenize.tokenize(BytesIO(tokens[index].string.strip(f'defProc {tokens[index+1].string}').strip('(').strip(')').replace(" ","").encode('utf-8')).readline)
                    
                    if check_token_sequence(string_proc):
                        pass
                    
                    if tokens[index+4].string == "{":
                        pass
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

#print(parse_execution(tokens))

#parse_execution(tokens)

"""
parse_execution(tokens)
print(list_procedures)
"""



