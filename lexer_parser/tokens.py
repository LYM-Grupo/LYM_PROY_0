#lexer_parser: Contiene archivos relacionados con el análisis léxico y sintáctico.
#tokens.py: Define clases o estructuras para representar los tokens.

def tokenizer(ruta_archivo):
    with open(ruta_archivo, "r") as file:
        for line in file:
            print(line.strip())
#lexer_parser: Contiene archivos relacionados con el análisis léxico y sintáctico.
#tokens.py: Define clases o estructuras para representar los tokens.

import tokenize
from io import BytesIO

conditions=["facing","can","not"]
#conditions=[{"key":"facing","args":1,"type_1": "orientation"},
            #{"key":"can","args":1,"type_1": "built_in_function"}]

values_parameters={"orientation":["north","south","east","west"],"direction":["left","right","around"]}
dict_variables={}
dict_procedures={}
list_built_in_function=["jump","walk","leap","turn","turninto","drop","get","grab","letgo","nop"]
list_dict_built_in_function=[   
    {"key":"walk","args":1,"type_1":"value"},
    {"key":"walk","args":2,"type_1":"value","type_2":"direction"},
    {"key":"walk","args":2,"type_1":"value","type_2":"orientation"},
    {"key":"leap","args":1,"type_1":"value"},
    {"key":"leap","args":2,"type_1":"value","type_2":"orientation"},
    {"key":"leap","args":2,"type_1":"value","type_2":"direction"},
    {"key":"turn","args":1,"type_1":"direction"},
    {"key":"turnto","args":1,"type_1":"orientation"},
    {"key":"drop","args":1,"type_1":"value"},
    {"key":"get","args":1,"type_1":"value"},
    {"key":"grab","args":2,"type_1":"value"},
    {"key":"letgo","args":1,"type_1":"value"},
    {"key":"nop","args":0,"type_1":"none"},
    {"key":"jump","args":2,"type_1":"value","type_2":"value"}
]

def verify_types(x,list_string_modified,defProc):#IMPORTANTE: Esto es mal toca corregirlo plus toca corregir lo del punto y coma 
    result=False
    if defProc.lower() in dict_procedures.keys():

        for z in range(0,len(x)):
            if x[z]["args"] == 1:
                
                if x[z]["type_1"] == "value" and (list_string_modified[0].lower() in dict_variables.keys() or list_string_modified[0].lower() in dict_procedures[defProc] or list_string_modified[0].isdigit()):
                    result = True
                
                elif x[z]["type_1"] == "orientation" and list_string_modified[0].lower() in values_parameters["orientation"]:
                    result = True
                
                elif x[z]["type_1"] == "direction" and (list_string_modified[0].lower() in values_parameters["direction"]):
                    result = True

            
            elif x[z]["args"] == 2:

                if x[z]["type_1"] == "value" and (list_string_modified[0].lower() in dict_variables.keys() or list_string_modified[0].lower() in dict_procedures[defProc] or list_string_modified[0].isdigit()):
                    
                    if x[z]["type_2"] == "orientation" and (list_string_modified[1].lower() in values_parameters["orientation"]):
                        result = True
                    
                    elif x[z]["type_2"] == "direction" and (list_string_modified[1].lower() in values_parameters["direction"]):
                        result = True

                    elif x[z]["type_2"] == "value" and (list_string_modified[1].lower() in dict_variables.keys() or list_string_modified[1].lower() in dict_procedures[defProc] or list_string_modified[1].isdigit()):
                        result = True
            elif  x[z]["args"] == 0 and x[z]["type_1"]=='none':
                    
                    result = True
            else:
                return False
        return result
    elif defProc.lower()=='':

        for z in range(0,len(x)):
            if x[z]["args"] == 1:
                
                if x[z]["type_1"] == "value" and (list_string_modified[0].lower() in dict_variables.keys() or list_string_modified[0].isdigit()):
                    result = True
                
                elif x[z]["type_1"] == "orientation" and list_string_modified[0].lower() in values_parameters["orientation"]:
                    result = True
                
                elif x[z]["type_1"] == "direction" and (list_string_modified[0].lower() in values_parameters["direction"]):
                    result = True

            
            elif x[z]["args"] == 2:

                if x[z]["type_1"] == "value" and (list_string_modified[0].lower() in dict_variables.keys() or list_string_modified[0].isdigit()):
                    
                    if x[z]["type_2"] == "orientation" and (list_string_modified[1].lower() in values_parameters["orientation"]):
                        result = True
                    
                    elif x[z]["type_2"] == "direction" and (list_string_modified[1].lower() in values_parameters["direction"]):
                        result = True

                    elif x[z]["type_2"] == "value" and (list_string_modified[1].lower() in dict_variables.keys() or list_string_modified[1].isdigit()):
                        result = True
            elif  x[z]["args"] == 0 and x[z]["type_1"]=='none':
                    
                    result = True
            else:
                return False
        return result
    else:
        return False

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
#IMPORTANTE: ARREGLAR TODOS LOS NOP
def parse_while_control_structure(list_blocks,string,last_line):
    result= False,len(list_blocks)
    i=0
    
    length = len(list_blocks)-1 
    while i< length:

        if (list_blocks[i].line.strip()[-1] == '}' and list_blocks[i].line.replace(' ','').strip().lower()==last_line) or (list_blocks[i].line.strip()[-1] == ';' and list_blocks[i].line.replace(' ','').strip().lower()!=last_line):

                #search_list_dict_built_in_function()
            if list_blocks[i+1].string.lower() == "not" and list_blocks[i+2].string.lower() == ':':
                
                if list_blocks[i+3].string.lower() == "facing" and list_blocks[i+4].string.lower() =='(' and list_blocks[i+5].string.lower() in values_parameters["orientation"] and list_blocks[i+6].string.lower() == ')':
                    string_block_code = list_blocks[i].line[list_blocks[i].line.find('{')+1:list_blocks[i].line.find('}')].replace(' ','')
                    list_tokens=list(tokenize.tokenize(BytesIO(string_block_code.encode('utf-8')).readline))[1:-1]
                    string_modified=string_block_code.replace(list_tokens[0].string.lower(),'').strip()[1:-1]
                        
                    if len(string_modified)!=0:
                        list_string_modified= string_modified.split(',')
                        x= search_list_dict_built_in_function(list_tokens[0].string.lower(),list_dict_built_in_function,len(list_string_modified))
                        if len(x)!=0:
                            if verify_types(x,list_string_modified,string):
                                return True ,len(list_blocks)
                            else:
                                return False ,len(list_blocks)
                
                elif list_blocks[i+3].string.lower() == "can" and list_blocks[i+4].string.lower() == '(':
                    while_index = list_blocks[i].line.find('while')
                    string_modified = list_blocks[i].line[while_index+5:list_blocks[i].line.find('{',while_index)].replace('can','').replace('not','').replace(':','').strip()
                    
                    if string_modified[-1] == ')':
                        string_modified = string_modified[1:-1].replace(' ','')
                        list_tokens=list(tokenize.tokenize(BytesIO(string_modified.encode('utf-8')).readline))[1:-1]
                        
                        string_modified = string_modified.replace(list_tokens[0].string.lower(),'').strip()[1:-1]

                        if len(string_modified)!=0:
                            list_string_modified =string_modified.split(',')
                            x = search_list_dict_built_in_function(list_tokens[0].string.lower(),list_dict_built_in_function,len(list_string_modified))
                            
                            if len(x)!=0:
                                
                                if verify_types(x,list_string_modified,string):

                                    string_modified_2=list_blocks[i].line[list_blocks[i].line.find('{')+1:list_blocks[i].line.find('}')].replace(' ','')
                                    list_tokens_2=list(tokenize.tokenize(BytesIO(string_modified_2.encode('utf-8')).readline))[1:-1]
                                    string_modified_2= string_modified_2.replace(list_tokens_2[0].string.lower(),'').strip()[1:-1]
                                    
                                    if len(string_modified_2) !=0:
                                        list_string_modified_2 = string_modified_2.split(',')
                                        y = search_list_dict_built_in_function(list_tokens_2[0].string.lower(),list_dict_built_in_function,len(list_string_modified_2))
                                        if len(y)!=0:
                                            
                                            if verify_types(y,list_string_modified_2,string):
                                                return True ,len(list_blocks)
                                            else:
                                                return False ,len(list_blocks)
                                    
                                else:
                                    return False,len(list_blocks)
                                
                            else:
                                return False,len(list_blocks)
                else:
                    return False
            elif list_blocks[i+1].string.lower() == "can" and list_blocks[i+2].string.lower() == '(':
                while_index = list_blocks[i].line.find('while')
                string_modified = list_blocks[i].line[while_index+5:list_blocks[i].line.find('{',while_index)].replace('can','').strip()
                
                if string_modified[-1] == ')':
                    string_modified = string_modified[1:-1].replace(' ','')
                    
                    list_tokens=list(tokenize.tokenize(BytesIO(string_modified.encode('utf-8')).readline))[1:-1]
                    
                    string_modified = string_modified.replace(list_tokens[0].string.lower(),'').strip()[1:-1]

                    if len(string_modified)!=0:
                        list_string_modified =string_modified.split(',')
                        x = search_list_dict_built_in_function(list_tokens[0].string.lower(),list_dict_built_in_function,len(list_string_modified))
                        
                        if len(x)!=0:
                            
                            if verify_types(x,list_string_modified,string):

                                string_modified_2=list_blocks[i].line[list_blocks[i].line.find('{')+1:list_blocks[i].line.find('}')].replace(' ','')
                                list_tokens_2=list(tokenize.tokenize(BytesIO(string_modified_2.encode('utf-8')).readline))[1:-1]
                                string_modified_2= string_modified_2.replace(list_tokens_2[0].string.lower(),'').strip()[1:-1]
                                
                                if len(string_modified_2) !=0:
                                    list_string_modified_2 = string_modified_2.split(',')
                                    y = search_list_dict_built_in_function(list_tokens_2[0].string.lower(),list_dict_built_in_function,len(list_string_modified_2))
                                    if len(y)!=0:
                                        
                                        if verify_types(y,list_string_modified_2,string):
                                            return True ,len(list_blocks)
                                        else:
                                            return False ,len(list_blocks)
                            else:
                                return False,len(list_blocks)
                            
                        else:
                            return False,len(list_blocks)

            elif list_blocks[i+1].string.lower() == "facing" and list_blocks[i+2].string.lower() =='(' and list_blocks[i+3].string.lower() in values_parameters["orientation"] and list_blocks[i+4].string.lower() == ')':
                string_block_code = list_blocks[i].line[list_blocks[i].line.find('{')+1:list_blocks[i].line.find('}')].replace(' ','')
                list_tokens=list(tokenize.tokenize(BytesIO(string_block_code.encode('utf-8')).readline))[1:-1]
                string_modified=string_block_code.replace(list_tokens[0].string.lower(),'').strip()[1:-1]
                
                if len(string_modified)!=0:
                    list_string_modified= string_modified.split(',')
                    x= search_list_dict_built_in_function(list_tokens[0].string.lower(),list_dict_built_in_function,len(list_string_modified))
                    if len(x)!=0:
                        if verify_types(x,list_string_modified,string):
                            return True ,len(list_blocks)
                        else:
                            return False ,len(list_blocks)
            else:
                return False , len(list_blocks)

        elif list_blocks[i].line.strip()[-1] == '{':
            pass
        i+=1
    return result
def code_blocks(list_blocks):
    print(list_blocks)
def parse_definition_defProc(list_blocks,defProc):
    #Faltan hacer varias cosas porque las funciones tambien permiten recursion de las misma funcion y llamado de otras funcion dentro de la misma funcion 
    #Falta otra cosa que es la verificacion del orden de los argumentos de una built-in function
    if list_blocks[-1].string == '}' and list_blocks[0]=='{':
        list_blocks=list_blocks[1:-1]
    
    length = len(list_blocks)
    if list_blocks[-1].string == ')' or list_blocks[-1].string == '}':
        
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

                elif line[-1] == ')' and list_blocks[i+1].string == '(' and line==list_blocks[-1].line.replace(' ','').strip().lower():#:#Aca esta el error de las comillas

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
                      
                    elif line[-1] == ')' and  list_blocks[i+1].string == '('  and line==list_blocks[-1].line.replace(' ','').strip().lower():
                        
                        if not(list_blocks[i].string.lower() == defProc.lower() and len(string_modified.split(',')) == len(dict_procedures[defProc]) and check_token_sequence_defProc_brackets(list(tokenize.tokenize(BytesIO(string_modified.encode('utf-8')).readline)))):
                            return False
                        
                        elif not(list_blocks[i].string.lower() in dict_procedures.keys() and len(dict_procedures[list_blocks[i].string.lower()]) == len(string_modified.split(',')) and check_token_sequence_defProc_brackets(list(tokenize.tokenize(BytesIO(string_modified.encode('utf-8')).readline)))):
                            return False
                    else:
                        return False
                else:

                    if line[-1] == ';' and list_blocks[i+1].string == '(' and line.replace(';','')[-1] == ')':
                        
                        if not(list_blocks[i].string.lower() in dict_procedures.keys() and len(dict_procedures[list_blocks[i].string.lower()])== len(string_modified.split())):
                            return False
                        
                    elif line[-1] == ')' and  list_blocks[i+1].string == '(' and line==list_blocks[-1].line.replace(' ','').strip().lower():

                        if not(list_blocks[i].string.lower() in dict_procedures.keys() and len(dict_procedures[list_blocks[i].string.lower()])== len(string_modified.split())):
                            return False
                    else:
                        return False
                    
            elif list_blocks[i].string.lower() == "while":
                
                search_position_variable = search_position(list_while_blocks,(list_blocks[i].start[0],list_blocks[i].start[1]))
                if search_position_variable[0]:
                    function=parse_while_control_structure(search_position_variable[1],defProc.lower(),list_blocks[-1].line.replace(' ','').strip().lower())
                    if function[0]:
                        i+=(function[1])
                    else:
                        return False

            elif list_blocks[i].string.lower() == "if":
                number_of_tokens=list(tokenize.tokenize(BytesIO(list_blocks[i].line.lower().strip().encode('utf-8')).readline))[1:-1]
                index_if = list_blocks[i].line.lower().find('if')
                index_key = list_blocks[i].line.lower().find('{',index_if)

                string_block_code=list_blocks[i].line.lower()[index_if+2:index_key].replace(' ','').strip()

                if list_blocks[i+1].string == 'can':
                    string_modified=string_block_code.replace('can','')[1:-1].strip()
                    
                    list_tokens=list(tokenize.tokenize(BytesIO(string_modified.encode('utf-8')).readline))[1:-1]
                    list_string_modified= string_modified.replace(list_tokens[0].string.lower(),'')[1:-1].split(',')
                    
                    if list_string_modified[0] == '' and list_tokens[0].string.lower()=='nop':
                        x=[{"key":"nop","args":0,"type_1":"none"}]
                    else:
                        x=search_list_dict_built_in_function(list_tokens[0].string.lower(),list_dict_built_in_function,len(list_string_modified))
                    if len(x) !=0:#tenemos que verificar que el numero de  argumentos en la funcion sea el correcto
                             
                        if verify_types(x,list_string_modified,defProc):
                            first_index=list_blocks[i].line.lower().find('{')
                            second_index=list_blocks[i].line.lower().find('}')
                            
                            first_block_code=list_blocks[i].line.lower()[first_index+1:second_index].replace(' ','').strip()

                            list_tokens_2=list(tokenize.tokenize(BytesIO(first_block_code.encode('utf-8')).readline))[1:-1]
                            list_string_modified_2= first_block_code.replace(list_tokens_2[0].string.lower(),'')[1:-1].split(',')
                           
                            if list_string_modified_2[0] == '' and list_tokens_2[0].string.lower()=='nop':
                                y=[{"key":"nop","args":0,"type_1":"none"}]
                            else:
                                y=search_list_dict_built_in_function(list_tokens_2[0].string.lower(),list_dict_built_in_function,len(list_string_modified_2))
                            if len(y) !=0:
                                
                                if verify_types(y,list_string_modified_2,defProc):
                                    
                                    string_else_block=list_blocks[i].line[list_blocks[i].line.find("else")+4:].replace(' ','').strip()
                                    
                                    if string_else_block[-1]=='}' and string_else_block[0]=='{': #arreglar esto para los ;
                                        list_tokens_3=list(tokenize.tokenize(BytesIO(string_else_block.encode('utf-8')).readline))[1:-1]
                                        list_string_modified_3 = string_else_block.replace(list_tokens_3[0].string.lower(),'')[1:-1].split(',')
                                        if list_string_modified_3[0]=='' and list_tokens_3[0].string.lower()== 'nop':#Aqui esta lo del nop IMPORTANTE 
                                            z=[{"key":"nop","args":0,"type_1":"none"}]
                                        else:
                                            z=search_list_dict_built_in_function(list_tokens_3[0].string.lower(),list_dict_built_in_function,len(list_string_modified_3))
                                            
                                        if len(z) !=0:
                                                
                                            if verify_types(z,list_string_modified_3,defProc):
                                                i+=len(number_of_tokens)-1
                                            else:
                                                return False
                                        
                                        else:
                                            return False 
                                    else:
                                        return False
                            else:
                                return False
                    else:
                        return False
                elif list_blocks[i+1].string.lower() == 'facing' and list_blocks[i+2].string=='(' and list_blocks[i+3].string.lower() in values_parameters['orientation'] and list_blocks[i+4].string==')':
                    index_init=list_blocks[i].line.find('{')
                    index_end=list_blocks[i].line.find('}')
                   
                    if index_init== -1 or index_end == -1:
                        return False
    
                    string_modified = list_blocks[i].line[index_init+1:index_end].lower().replace(' ','').strip()
                    
                    list_tokens=list(tokenize.tokenize(BytesIO(string_modified.encode('utf-8')).readline))[1:-1]
                    list_string_modified = string_modified.replace(list_tokens[0].string,'').replace(' ','').strip()[1:-1].split(',')
                    
                    if list_string_modified[0] == '' and list_tokens[0].string.lower()=='nop':
                        x=[{"key":"nop","args":0,"type_1":"none"}]
                    else:
                        x=search_list_dict_built_in_function(list_tokens[0].string.lower(),list_dict_built_in_function,len(list_string_modified))
                    
                    if len(x)!=0:
                        
                        if verify_types(x,list_string_modified,defProc):
                            string_modified_2 = list_blocks[i].line[list_blocks[i].line.find("else")+4:].lower().replace(' ','').strip()
                            if string_modified_2[0] == '{' and string_modified_2[-1] == '}':
                                string_modified_2 = string_modified_2[1:-1]

                                list_tokens_2 = list(tokenize.tokenize(BytesIO(string_modified_2.encode('utf-8')).readline))[1:-1]
                                list_string_modified_2 = string_modified_2.replace(list_tokens_2[0].string,'').replace(' ','').strip()[1:-1].split(',')
                                
                                if list_string_modified_2[0] == '' and list_tokens_2[0].string.lower()=='nop':
                                    y = [{"key":"nop","args":0,"type_1":"none"}]
                                else:
                                    y = search_list_dict_built_in_function(list_tokens_2[0].string.lower(),list_dict_built_in_function,len(list_string_modified_2))
                                if len(y)!=0:
                                    i+=len(number_of_tokens)-1
                                else:
                                    return False
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                    

                elif list_blocks[i+1].string.lower() == 'not' and list_blocks[i+2].string.lower() == ':':

                    if list_blocks[i+3].string.lower() == 'facing' and list_blocks[i+4].string.lower() == '(' and list_blocks[i+5].string.lower() in values_parameters['orientation'] and list_blocks[i+6].string.lower() == ')':

                        index_init=list_blocks[i].line.find('{')
                        index_end=list_blocks[i].line.find('}')
                    
                        if index_init== -1 or index_end == -1:
                            return False
        
                        string_modified = list_blocks[i].line[index_init+1:index_end].lower().replace(' ','').strip()
                        
                        list_tokens=list(tokenize.tokenize(BytesIO(string_modified.encode('utf-8')).readline))[1:-1]
                        list_string_modified = string_modified.replace(list_tokens[0].string,'').replace(' ','').strip()[1:-1].split(',')
                        
                        if list_string_modified[0] == '' and list_tokens[0].string.lower()=='nop':
                            x=[{"key":"nop","args":0,"type_1":"none"}]
                        else:
                            x=search_list_dict_built_in_function(list_tokens[0].string.lower(),list_dict_built_in_function,len(list_string_modified))
                        
                        if len(x)!=0:
                            
                            if verify_types(x,list_string_modified,defProc):
                                string_modified_2 = list_blocks[i].line[list_blocks[i].line.find("else")+4:].lower().replace(' ','').strip()
                                if string_modified_2[0] == '{' and string_modified_2[-1] == '}':
                                    string_modified_2 = string_modified_2[1:-1]

                                    list_tokens_2 = list(tokenize.tokenize(BytesIO(string_modified_2.encode('utf-8')).readline))[1:-1]
                                    list_string_modified_2 = string_modified_2.replace(list_tokens_2[0].string,'').replace(' ','').strip()[1:-1].split(',')
                                    
                                    if list_string_modified_2[0] == '' and list_tokens_2[0].string.lower()=='nop':
                                        y = [{"key":"nop","args":0,"type_1":"none"}]
                                    else:
                                        y = search_list_dict_built_in_function(list_tokens_2[0].string.lower(),list_dict_built_in_function,len(list_string_modified_2))
                                    if len(y)!=0:
                                        i+=len(number_of_tokens)-1
                                    else:
                                        return False
                                else:
                                    return False
                            else:
                                return False
                        else:
                            return False
                        
                    elif list_blocks[i+3].string.lower() == 'can':
                        
                        string_modified=string_block_code.replace('can','').replace('not','').replace(':','').strip().replace(' ','')[1:-1]
                        
                        list_tokens=list(tokenize.tokenize(BytesIO(string_modified.encode('utf-8')).readline))[1:-1]
                        
                        list_string_modified= string_modified.replace(list_tokens[0].string.lower(),'')[1:-1].split(',')
                        
                        if list_string_modified[0] == '' and list_tokens[0].string.lower()=='nop':
                            x=[{"key":"nop","args":0,"type_1":"none"}]
                        else:
                            x=search_list_dict_built_in_function(list_tokens[0].string.lower(),list_dict_built_in_function,len(list_string_modified))
                        if len(x) !=0:#tenemos que verificar que el numero de  argumentos en la funcion sea el correcto
                                
                            if verify_types(x,list_string_modified,defProc):
                                
                                first_index=list_blocks[i].line.lower().find('{')
                                second_index=list_blocks[i].line.lower().find('}')
                                
                                first_block_code=list_blocks[i].line.lower()[first_index+1:second_index].replace(' ','').strip()

                                list_tokens_2=list(tokenize.tokenize(BytesIO(first_block_code.encode('utf-8')).readline))[1:-1]
                                list_string_modified_2= first_block_code.replace(list_tokens_2[0].string.lower(),'')[1:-1].split(',')
                            
                                if list_string_modified_2[0] == '' and list_tokens_2[0].string.lower()=='nop':
                                    y=[{"key":"nop","args":0,"type_1":"none"}]
                                else:
                                    y=search_list_dict_built_in_function(list_tokens_2[0].string.lower(),list_dict_built_in_function,len(list_string_modified_2))
                                if len(y) !=0:
                                    
                                    if verify_types(y,list_string_modified_2,defProc):
                                        
                                        string_else_block=list_blocks[i].line[list_blocks[i].line.find("else")+4:].replace(' ','').strip()
                                        
                                        if string_else_block[-1]=='}' and string_else_block[0]=='{': #arreglar esto para los ;
        
                                            string_else_block=string_else_block[1:-1]
                                            list_tokens_3=list(tokenize.tokenize(BytesIO(string_else_block.encode('utf-8')).readline))[1:-1]
                                            list_string_modified_3 = string_else_block.replace(list_tokens_3[0].string.lower(),'')[1:-1].split(',')
                                            if list_string_modified_3[0]=='' and list_tokens_3[0].string.lower()== 'nop':#Aqui esta lo del nop IMPORTANTE 
                                                z=[{"key":"nop","args":0,"type_1":"none"}]
                                            else:
                                                z=search_list_dict_built_in_function(list_tokens_3[0].string.lower(),list_dict_built_in_function,len(list_string_modified_3))
                                            
                                            if len(z) !=0:
                                                
                                                if verify_types(z,list_string_modified_3,defProc):
                                                    i+=len(number_of_tokens)-1
                                                else:
                                                    return False
                                            
                                            else:
                                                return False 
                                        else:
                                            return False
                                else:
                                    return False
                    
                                      

            elif list_blocks[i].string.lower() == "repeat":
                print('hola')
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
                        print(search_position_variable[1])
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
                                    print(search_position_variable[1])
                                    return False
                                       
                            else:
                                return False
                        else:
                            return False
                else:
                    return False
                
            else:
                return False
        #-------------------------------------------------------------------------------------------------------------------------------------------
        #PARSER CODE BLOCKS
        
    elif tokens[index].string.lower() == '{':
        
        search_position_variable=search_position(list_block,(tokens[index].start[0]+1,0))
        if search_position_variable[0]:
            
            if not(code_blocks(search_position_variable[1])):
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
        
# mac : /Users/fodepixofarfan/Downloads/LYM_PROY_0/sample_program.txt
# linux : /home/keith/Downloads/LYM_PROY_0/sample_program.txt
tokens = tokenize_text_from_file("/Users/fodepixofarfan/Downloads/LYM_PROY_0/sample_sample.txt")
#try:
#    print(parse_execution(tokens))
#except:
#    print("False")
list_block=extract_code_blocks(tokens)
list_while_blocks = extract_while_blocks(tokens)
#print(list_while_blocks)
print(parse_execution(tokens))


"""
parse_execution(tokens)
print(list_procedures)
"""