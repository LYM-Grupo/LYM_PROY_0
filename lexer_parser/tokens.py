#lexer_parser: Contiene archivos relacionados con el análisis léxico y sintáctico.
#tokens.py: Define clases o estructuras para representar los tokens.

import tokenize
from io import BytesIO

conditions=[{"key":"facing","args":1,"type_1": "orientation"},
            {"key":"can","args":1,"type_1": "built_in_function"},
            {"key":"not","args":1,"type_1": "condition"}]

values_parameters={"orientation":["north","south","east","west"],"direction":["left","right","around"]}
dict_variables={}
dict_procedures={}
list_built_in_function=["jump","walk","leap","turn","turninto","drop","get","grab","letGo","nop"]
list_dict_built_in_function=[   
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

def verify_types(x,list_string_modified,defProc):#Esto es mal toca corregirlo plus toca corregir lo del punto y coma 
    for z in range(0,len(x)):
        if x[z]["args"] == 1:
            #print(dict_procedures)#IMPORTANTE Esto es mal 
            if x[z]["type_1"] == "value" and (list_string_modified[0] in dict_variables.keys() or list_string_modified[0] in dict_procedures[defProc] or list_string_modified[0].isdigit()):
                return False
            
            elif x[z]["type_1"] == "orientation" and not(list_string_modified[0].lower() in values_parameters["orientation"]):
                return False
            
            elif x[z]["type_1"] == "direction" and not(list_string_modified[0].lower() in values_parameters["direction"]):
                return False
        
        elif x[z]["args"] == 2:
            print(x[z]["type_2"] == "direction")
            print(list_string_modified[1].lower() in values_parameters["direction"])
            print('\n')
            print(x[z]["type_2"] == "orientation")
            print(list_string_modified[1].lower() in values_parameters["orientation"])
            print('\n')

            if x[z]["type_1"] == "value" and (list_string_modified[0] in dict_variables.keys() or list_string_modified[0] in dict_procedures[defProc] or list_string_modified[0].isdigit()):

                if x[z]["type_2"] == "orientation" and not(list_string_modified[1].lower() in values_parameters["orientation"]):
                    return False
                
                elif x[z]["type_2"] == "direction" and not(list_string_modified[1].lower() in values_parameters["direction"]):
                    return False
                
            elif x[z]["type_1"] == "orientation" and not(list_string_modified[0].lower() in values_parameters["orientation"]):
                return False
            
            elif x[z]["type_1"] == "direction" and not(list_string_modified[0].lower() in values_parameters["direction"]):
                return False

        else:
            return False
    return True

def search_list_dict_built_in_function(key,list_dict,len_arguments):
    list_posibilities=[] 
    for i in list_dict:
        if i["key"] == key and i["args"] == len_arguments:
            list_posibilities.append(i)

    return list_posibilities

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
        if tokens[1].type == tokenize.NAME:
            
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
        else:
            return False
    return result

def extract_while_blocks(tokens):
    while_blocks = []
    block = []
    depth = 0
    within_while = False

    for token in tokens:
        if token.string == 'while':
            depth += 1
            within_while = True
            if depth == 1:
                block = [token]
        elif token.string == '}':
            depth -= 1
            if depth == 0 and within_while:
                block.append(token)
                while_blocks.append(block)
                within_while = False
        elif depth > 0 and within_while:
            block.append(token)
    
    return while_blocks


def check_token_sequence_defProc_brackets(tokens):
    result= False
    for i in range(0,len(tokens)-3):
        if tokens[1].type == tokenize.NAME or tokens[1].type == tokenize.NUMBER:
            
            if tokens[i].type == tokenize.NAME and tokens[i].string in dict_variables.keys():

                if tokens[i+1].type == tokenize.OP and tokens[i+1].string == ',':
                    result = True
                else:
                    return False

            elif tokens[i].type == tokenize.NUMBER:

                if tokens[i+1].type == tokenize.OP and tokens[i+1].string == ',':
                    result = True
                else:
                    return False
                
            elif tokens[i].type == tokenize.OP and tokens[i].string == ',':

                if tokens[i+1].type == tokenize.NAME and tokens[i+1].string in dict_variables.keys():
                    result = True

                elif tokens[i+1].type == tokenize.NUMBER:
                    result = True 

                else:
                    return False
        else:
            return False
    return result

def parse_definition_control_structures():
    pass

def parse_definition_defProc(list_blocks,defProc):
    #Faltan hacer varias cosas porque las funciones tambien permiten recursion de las misma funcion y llamado de otras funcion dentro de la misma funcion 
    #Falta otra cosa que es la verificacion del orden de los argumentos de una built-in function
    list_blocks=list_blocks[1:-1]
    length = len(list_blocks)
    if list_blocks[-1].string == ')':
        i=0
        while i<length:# IMPORTANTE: Necesitamos elminar bloques de codigo de while aumentando el numero de lineas de acuerdo a la cantidad de tokens presentes en el bloque 
        #for i in range(0,len(list_blocks)):
            
            if list_blocks[i].string.lower() in list_built_in_function:
            
                line=list_blocks[i].line.replace(' ','').strip()#Es necesario poner strip para poder leer el ultimo elemento 
                
                if line[-1] == ';' and list_blocks[i+1].string == '(' and line.replace(';','')[-1] == ')':

                    string_modified = line.replace(list_blocks[i].string.lower(),'').replace('(','').replace(')','').replace('\n','').replace(';','')

                    #aca si list string modified es vacio entonces solo se verifica el built in function o el procedimiento
                    if len(string_modified) !=0:
                        
                        #IMPORTANTE : eliminar check_token_sequence_defProc

                        list_string_modified = string_modified.split(',') 
                            
                        x=search_list_dict_built_in_function(list_blocks[i].string.lower(),list_dict_built_in_function,len(list_string_modified))
                        if len(x) !=0:#tenemos que verificar que el numero de  argumentos en la funcion sea el correcto
                             
                            if not verify_types(x,list_string_modified,defProc):
                                return False
                                    
                        else:
                            return False

                    else:
                        if list_blocks[i].string.lower() != "nop":
                            return False
                        
                elif line[-1] == ')' and list_blocks[i+1].string == '(':#Aca esta el error de las comillas

                    string_modified = line.strip().replace(list_blocks[i].string.lower(),'').replace('(','').replace(')','').replace('\n','').replace(';','')

                    #aca si list string modified es vacio entonces solo se verifica el built in function o el procedimiento
                    if len(string_modified) !=0:

                        list_string_modified = string_modified.split(',') 
                            
                        x=search_list_dict_built_in_function(list_blocks[i].string.lower(),list_dict_built_in_function,len(list_string_modified))
                        if len(x) !=0:#tenemos que verificar que el numero de  argumentos en la funcion sea el correcto
                             
                            if not verify_types(x,list_string_modified,defProc.lower()):
                                return False
                                    
                        else:
                            return False

                    else:
                        if list_blocks[i].string.lower() != "nop":
                            return False
                
            elif list_blocks[i].string.lower() in dict_procedures.keys():

                line=list_blocks[i].line.replace(' ','').strip().lower()

                string_modified = line.replace(list_blocks[i].string.lower(),'').replace('(','').replace(')','').replace('\n','').replace(';','')
                
                
                if len(string_modified)!=0:
                    if line[-1] == ';' and list_blocks[i+1].string == '(' and line.replace(';','')[-1] == ')':
                        
                        if not(list_blocks[i].string.lower() == defProc.lower() and len(string_modified.split(',')) == len(dict_procedures[defProc]) and check_token_sequence_defProc_brackets(list(tokenize.tokenize(BytesIO(string_modified.encode('utf-8')).readline)))):
                            return False
                        
                        elif not(list_blocks[i].string.lower() in dict_procedures.keys() and len(dict_procedures[list_blocks[i].string.lower()])== len(string_modified.split(',')) and check_token_sequence_defProc_brackets(list(tokenize.tokenize(BytesIO(string_modified.encode('utf-8')).readline)))):
                            return False
                      
                    elif line[-1] == ')' and  list_blocks[i+1].string == '(':
                        
                        if not(list_blocks[i].string.lower() == defProc.lower() and len(string_modified.split(',')) == len(dict_procedures[defProc]) and check_token_sequence_defProc_brackets(list(tokenize.tokenize(BytesIO(string_modified.encode('utf-8')).readline)))):
                            return False
                        
                        elif not(list_blocks[i].string.lower() in dict_procedures.keys() and len(dict_procedures[list_blocks[i].string.lower()]) == len(string_modified.split(',')) and check_token_sequence_defProc_brackets(list(tokenize.tokenize(BytesIO(string_modified.encode('utf-8')).readline)))):
                            return False
                else:

                    if line[-1] == ';' and list_blocks[i+1].string == '(' and line.replace(';','')[-1] == ')':
                        
                        if not(list_blocks[i].string.lower() in dict_procedures.keys() and len(dict_procedures[list_blocks[i].string.lower()])== len(string_modified.split())):
                            return False
                        
                    elif line[-1] == ')' and  list_blocks[i+1].string == '(':

                        if not(list_blocks[i].string.lower() in dict_procedures.keys() and len(dict_procedures[list_blocks[i].string.lower()])== len(string_modified.split())):
                            return False
            i+=1   
    else:
        return False

    return True

def parse_definition(tokens, index):

    if tokens[index].string.lower() in ['defvar', 'defproc']:#Definimos el procedimiento para verificar las definiciones de las funciones y las variables 
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------
        #PARSER VARIABLE DEFINITION
        if tokens[index].string == 'defVar':#Definimos la sintaxis y semantica para las definicion de las variables

            if tokens[index+1].type == tokenize.NAME:#la variable tiene que ser de tipo NAME no puede ser operador

                if tokens[index+2].type == tokenize.NAME and tokens[index+2].string in dict_variables.keys():#search_list_dict(list_dict_variables,tokens[index+2].string):#Si es una variable que es NAME entonces tienes que estar definida anteriormente
                    dict_variables[str(tokens[index+1].string).lower()] = tokens[index+2].string
                    #list_dict_variables.append({str(tokens[index+1].string):tokens[index+2].string})
                    
                elif tokens[index+2].type == tokenize.NUMBER:#Si es numero 
                    dict_variables[str(tokens[index+1].string).lower()] = tokens[index+2].string
                    #list_dict_variables.append({str(tokens[index+1].string):tokens[index+2].string})
                    
                else:
                    
                    return False
            else:
                
                return False
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------
        #PARSER PROCEDURE DEFINITION
        elif tokens[index].string.lower() == 'defproc':#Definimos la sintaxis y semantica para la defincion de las funciones
            
            if tokens[index+1].type == tokenize.NAME:
                if tokens[index+2].string == "(" and tokens[index].line.strip()[-1] == ")":

                    string_modified= tokens[index].line.strip().lower().replace('defproc','').replace(tokens[index+1].string.lower(),'').replace('(','').replace(')','').replace(" ","")

                    if len(string_modified)==0:
                        
                        dict_procedures[tokens[index+1].string.lower()]=[]
                        #list_dict_procedures.append({tokens[index+1].string:[]})
                        
                        search_position_variable=search_position(list_block,(tokens[index].start[0]+1,0))
                        if search_position_variable[0]:#si tiene el mismo identificador que el del procedmiento asi sea sumandole 1 al start y end
                            if not(parse_definition_defProc(search_position_variable[1],tokens[index+1].string.lower())):
                                return False
                            
                        else:
                            return False
                    else:

                        string_proc = list(tokenize.tokenize(BytesIO(string_modified.encode('utf-8')).readline))

                        if check_token_sequence_defProc(string_proc):

                            dict_procedures[tokens[index+1].string.lower()] = string_modified.replace('\n','').split(',')
                            #list_dict_procedures.append({tokens[index+1].string:string_modified.replace('\n','').split(',')})
                                 
                            search_position_variable = search_position(list_block,(tokens[index].start[0]+1,0))
                            if search_position_variable[0]:
                                if not(parse_definition_defProc(search_position_variable[1],tokens[index+1].string.lower())):
                                    return False
                                       
                            else:
                                return False
                        else:
                            return False
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
            return False
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
#list_while_blocks = extract_while_blocks(tokens)
print(parse_execution(tokens))


"""
parse_execution(tokens)
print(list_procedures)
"""