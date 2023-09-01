#lexer_parser: Contiene archivos relacionados con el análisis léxico y sintáctico.
#tokens.py: Define clases o estructuras para representar los tokens.

import tokenize
from io import BytesIO

values_parameters=[{"orientation":["north","south","east","west"]},{"direction":["left","right","around"]}]
list_dict_variables=[]
list_procedures=[]
list_built_function=[   
    {"key":"jump","args":2,"type_1":"value"},
    {"key":"walk","args":1,"type_1":"value"},
    {"key":"walk","args":2,"type_1":"value","type_2":"direction"},
    {"key":"walk","args":2,"type_1":"value","type_2":"orientation"},
    {"key":"leap","args":1,"type_1":"value"},
    {"key":"leap","args":2,"type_1":"value","type_2":"direction"},
    {"key":"leap","args":2,"type_1":"value","type_2":"direction"},
    {"key":"turn","args":1,"type_1":"direction"},
    {"key":"turnto","args":1,"type_1":"orientation"},
    {"key":"drop","args":1,"type_1":"value"},
    {"key":"get","args":1,"type_1":"value"},
    {"key":"grab","args":2,"type_1":"value"},
    {"key":"letGo","args":1,"type_1":"value"},
    {"key":"nop","args":0,"type_1":"None"}
]

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
                block = [token]
        elif token.string == '}':
            depth -= 1
            if depth == 0:
                block.append(token)
                code_blocks.append(block)
        elif depth > 0:
            block.append(token)

    return code_blocks

def search_position(list_block,target_coordinate):
    for i in list_block:
        for j in i:
            if j.start == target_coordinate:
                return True,i
    return False,i

def check_token_sequence_defProc(tokens):
    result = False 
    for i in range(0,len(tokens)-3):

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
#print(check_token_sequence(tokenize.tokenize(BytesIO("".encode('utf-8')).readline)))
def parse_definition_defProc():
    result="Hola"
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
                if tokens[index+2].string == "(" and tokens[index].line.strip()[-1] == ")":

                    string_modified= tokens[index].line.replace('defProc','').replace(str(tokens[index+1].string),'').replace('(','').replace(')','').replace(" ","")

                    
                    if len(string_modified)==0:

                        list_procedures.append({tokens[index+1].string:[]})
                        
                        search_position_variable=search_position(list_block,(tokens[index].start[0]+1,0))
                        if search_position_variable[0]:#si tiene el mismo identificador que el del procedmiento asi sea sumandole 1 al start y end
                            pass

                        else:
                            return False
                    else:

                        string_proc = list(tokenize.tokenize(BytesIO(string_modified.encode('utf-8')).readline))

                        if check_token_sequence_defProc(string_proc):

                            list_procedures.append({tokens[index+1].string:string_modified.replace('\n','').split(',')})
                                 
                            search_position_variable = search_position(list_block,(tokens[index].start[0]+1,0))
                            if search_position_variable[0]:
                                pass
                            else:
                                return False
                        else:
                            return False
                    #Aca se define el parser del inicio del procedimiento 
                    #if tokens[index+4].string == "{":
                        #pass
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
        
# mac : /Users/fodepixofarfan/Downloads/LYM_PROY_0/sample_program.txts
# linux : /home/keith/Downloads/LYM_PROY_0/sample_program.txt
tokens = tokenize_text_from_file("/home/keith/Downloads/LYM_PROY_0/sample_sample.txt")
#try:
#    print(parse_execution(tokens))
#except:
#    print("False")
list_block=extract_code_blocks(tokens)
#print(search_position(list_block,(2,0)))
print(parse_execution(tokens))
#print(list_procedures)
"""
parse_execution(tokens)
print(list_procedures)
"""