# Analizador lexico


import tokenize
from io import BytesIO
#Wordsprohibid:["walk","leap","turn","turnto","drop","get","grab","letgo","nop","repeat","times",'defVar','defProc']
#Words:["walk","leap","turn","turnto","drop","get","grab","letgo","nop"]

variablesCreadas = []  # Aca metere las variables de los DefVar y DefProcedure
variablesCreadasProcedimiento=[]

def Creacion(file_path,filtered_token_generator):
    file_path=("/Users/marcosrodrigo/Desktop/Lym Trabajo/sample_program.txt")
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    token_generator = tokenize.tokenize(BytesIO(text.encode('utf-8')).readline)
    #filtered_token_generator = []
    filters = [tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT,
               tokenize.NL]  # Borra las indentaciones, saltos de linea, espacios, etc.
    for token in token_generator:
        if token.type not in filters:
            filtered_token_generator.append(token)
    return filtered_token_generator


def ProcesamientoDatos(filtered_token_generator):
    NumeroDeInstruccionFija=1 # NO TOCAR
    flagError=False
    counter = 0

    for instruccion in filtered_token_generator:
        instruccionPosicion=filtered_token_generator[counter][NumeroDeInstruccionFija]# DIRECCION PARA ESCOGER
        if instruccionPosicion==("defVar"):
            counter+=1
            ProcesNombre,instruccionPosicionName = ProcesamientoName(filtered_token_generator, counter,NumeroDeInstruccionFija,variablesCreadas)
            if ProcesNombre==True and instruccionPosicionName not in variablesCreadas:
                variablesCreadas.append(instruccionPosicionName)
                counter += 1
                ProcesNumero,ignore = ProcesamientoNumber(filtered_token_generator, counter,NumeroDeInstruccionFija)
                if ProcesNumero==True:
                    flagError=True #Si es true quiere decir que el proceso esta haciendose bien
                    counter += 1
                else:
                    flagError=False # Si es False quiere decir que el proceso esta mal
                    break
            else:
                flagError=False
                break

        #ACA TODO PERFECTO


        elif instruccionPosicion==("defProc"):
            counter += 1
            ProcesNombre,instruccionPosicionName = ProcesamientoName(filtered_token_generator, counter,NumeroDeInstruccionFija,variablesCreadas)

            if ProcesNombre == True and (instruccionPosicionName not in variablesCreadasProcedimiento) and instruccionPosicionName not in variablesCreadas: #No puede haber un Procedimiento nombrado igual que una variable o otro procedimiento
                variablesCreadasProcedimiento.append(instruccionPosicionName)
                counter += 1
                r=counter+1
                instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
                ip2 = filtered_token_generator[r][NumeroDeInstruccionFija]
                procesoCorrecto,counter= procesoOperadores(filtered_token_generator,counter,NumeroDeInstruccionFija,variablesCreadas)

                if procesoCorrecto==False:
                    if instruccionPosicion==("(") and ip2==(")"):#Proceso Correcto Solo que no valido que hay entrada de # Lo cual tambien esta bien
                        r += 1 #Le sumo 1 para que quede en {
                        counter = r
                        IP2 = filtered_token_generator[counter][NumeroDeInstruccionFija]

                        bloqueProces, counter = procesoBloque(filtered_token_generator, r, NumeroDeInstruccionFija,variablesCreadas)

                        if bloqueProces == True:  # Las instrucciones dadas antes estan bien
                            flagError = True  # True si la instruccion esta bien
                            break
                        else:
                            flagError = False
                            break
                    else:
                        flagError = False
                        break

                if procesoCorrecto==True:
                    bloqueProces, counter = procesoBloque(filtered_token_generator, counter,NumeroDeInstruccionFija, variablesCreadas)
                    if bloqueProces==True: #Las instrucciones dadas antes estan bien
                        flagError=True #True si la instruccion esta bien
                        break
                    else:
                        flagError=False
                        break

    return flagError

def ProcesamientoName(filtered_token_generator,counter,NumeroDeInstruccionFija,variablesCreadas):
    instruccionPosicion=filtered_token_generator[counter][NumeroDeInstruccionFija]
    if instruccionPosicion.isalpha():
        ProcesamientoNombre = True
        if instruccionPosicion in variablesCreadas:
            ProcesamientoNombre=False
    else:
        ProcesamientoNombre=False


    return ProcesamientoNombre,instruccionPosicion

def ProcesamientoNumber(filtered_token_generator,counter,NumeroDeInstruccionFija):
    instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
    if instruccionPosicion.isdigit():
        ProcesamientoNombre = True
    else:
        ProcesamientoNombre = False

    return ProcesamientoNombre,instruccionPosicion

def procesoOperadores(filtered_token_generator, counter, NumeroDeInstruccionFija,variablesCreadas):
    instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
    parentesisCounter=0
    a = counter
    controlFinalOperador=True
    procesoCorrecto=False
    if instruccionPosicion==("("):
        counter+=1
        parentesisCounter+=1
        ControlComas = False
        procesoCorrecto = True
        while controlFinalOperador==True:
            procesoInterno, ControlComas, parentesisCounter = procesoInternoOperador(filtered_token_generator, counter,
                                                                                     NumeroDeInstruccionFija,
                                                                                     variablesCreadas,
                                                                                     parentesisCounter, procesoCorrecto,
                                                                                     ControlComas)
            counter += 1 #Sale y me deja en {
            a=counter
            if procesoInterno==False:
                controlFinalOperador=False
                procesoCorrecto=False #Alguna variable no esta dentro del rango de las definidas anteriormente
                break
            if parentesisCounter==2 and procesoInterno==True:
                controlFinalOperador=False
                procesoCorrecto=True
                break

    return procesoCorrecto,a #Si la lecutura estuvo bien y el cntador que se quedo


def procesoBloque(filtered_token_generator, counter, NumeroDeInstruccionFija, variablesCreadas):
    # BLOQUE DE CODIGO
    procesoCorrectoBloquue=False
    procesoCorrecto = True
    corchetesCounter = 0
    wordsImportant = ["jump", "walk", "leap", "turn", "turnto", "drop", "get", "grab", "letGo", "nop"]
    conditions =["if", "while" , "repeat"]
    instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
    if instruccionPosicion != ("{"):  # TODO ACA DEBE PARAR TODO
        procesoCorrectoBloquue = False

    if instruccionPosicion == ("{"):
        counter += 1
        corchetesCounter += 1
        while procesoCorrecto == True:
            ip = filtered_token_generator[counter][NumeroDeInstruccionFija]
            if ip in conditions:
                if ip==("if"):
                    verificarConditions,counter=VerificarCondicionales(filtered_token_generator, counter,NumeroDeInstruccionFija)
                    #Ya verifico el condition sigue verificar el Block
                    counter += 1
                    corcheteAbierto = filtered_token_generator[counter][NumeroDeInstruccionFija]

                    if corcheteAbierto==("{"):
                        corchetesCounterPte2=1
                        procesoCorrectoBloquue=True
                        counter += 1
                        bloque = filtered_token_generator[counter][NumeroDeInstruccionFija]
                        #ACA YA ESTA LA INSTRUCCION
                        validadorBloque,counter=validationOpIntern(filtered_token_generator, counter, NumeroDeInstruccionFija,bloque)
                        if validadorBloque ==True:
                            counter += 1
                            corcheteCerrado= filtered_token_generator[counter][NumeroDeInstruccionFija]
                            corchetesCounterPte2 += 1
                            if corcheteCerrado==('}'):
                                counter += 1
                                condition2 = filtered_token_generator[counter][NumeroDeInstruccionFija]
                                if condition2==("else"):
                                    counter += 1
                                    bloque = filtered_token_generator[counter][NumeroDeInstruccionFija]
                                    validadorBloque, counter = validationOpIntern(filtered_token_generator, counter,
                                                                          NumeroDeInstruccionFija, bloque)
                                    if validadorBloque==True:
                                        counter += 1
                                        posicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
                                        if posicion==("}"):
                                            corchetesCounter += 1
                                            procesoCorrectoBloquue=True
                                            return procesoCorrectoBloquue, counter

                                    else:
                                        procesoCorrectoBloquue=False
                                else:
                                    procesoCorrectoBloquue=False
                            else:
                                procesoCorrectoBloquue=False
                        else:
                            procesoCorrectoBloquue=False
                    else:
                        procesoCorrectoBloquue=False

                    pass

                if ip==("while"):
                    #Sigue condicion
                    verificarConditions,counter = VerificarCondicionales(filtered_token_generator, counter,NumeroDeInstruccionFija)
                    counter += 1
                    corcheteAbierto = filtered_token_generator[counter][NumeroDeInstruccionFija]

                    if corcheteAbierto == ("{"):
                        corchetesCounterPte2 = 1
                        procesoCorrectoBloquue = True
                        counter += 1
                        bloque = filtered_token_generator[counter][NumeroDeInstruccionFija]
                        validadorBloque, counter = validationOpIntern(filtered_token_generator, counter,NumeroDeInstruccionFija, bloque)
                        if validadorBloque == True: #TODO ACA LE PUEDO METER UN CICLO
                                counter += 1
                                corcheteCerrado = filtered_token_generator[counter][NumeroDeInstruccionFija]
                                corchetesCounterPte2 += 1
                                if corcheteCerrado == ('}'):
                                    counter += 1
                                    instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
                                    if instruccionPosicion==("}"):
                                        procesoCorrectoBloquue=True
                                        return procesoCorrectoBloquue, counter

                                    else:
                                        procesoCorrectoBloquue=False
                                    #counter += 1
                                else:
                                    instruccionPosicion=False
                        else:
                            instruccionPosicion=False

                if ip ==("repeat"):
                    counter+=1
                    verificarNumero=ProcesamientoNumber(filtered_token_generator, counter, NumeroDeInstruccionFija)
                    counter+=1
                    if verificarNumero==True:
                        instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
                        if instruccionPosicion ==("times"):
                            counter += 1
                            instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
                            if instruccionPosicion==("{"):
                                validadorBloque, counter = validationOpIntern(filtered_token_generator, counter,
                                                                              NumeroDeInstruccionFija, bloque)
                                counter += 1
                                if validadorBloque == True:  # TODO ACA LE PUEDO METER UN CICLO
                                    corcheteCerrado = filtered_token_generator[counter][NumeroDeInstruccionFija]
                                    corchetesCounterPte2 += 1
                                    if corcheteCerrado == ('}'):
                                        counter += 1
                                        instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
                                        if instruccionPosicion == ("}"):
                                            procesoCorrectoBloquue = True
                                            return procesoCorrectoBloquue, counter

                                        # counter += 1
                                        else:
                                            procesoCorrectoBloquue = False
                                    else:
                                        procesoCorrectoBloquue = False
                            else:
                                procesoCorrectoBloquue = False
                        else:
                            procesoCorrectoBloquue = False
                    else:
                        procesoCorrectoBloquue=False

            if ip in wordsImportant:

                verificacionBloqueCod,counter = bloqueCodigo(filtered_token_generator, counter, NumeroDeInstruccionFija,
                                                     variablesCreadas, corchetesCounter, procesoCorrecto,
                                                     wordsImportant)
                instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
                counter += 1
                counter2=counter
                counter2+=1
                instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
                instruccionPosicion2 = filtered_token_generator[counter2][NumeroDeInstruccionFija]
                counter += 1
                if verificacionBloqueCod == False:
                    procesoCorrecto=False
                    procesoCorrectoBloquue = False
                if verificacionBloqueCod==True:
                    if instruccionPosicion == (";") and instruccionPosicion2 != ("}"):
                        procesoCorrecto = True # Tiene que ser True para seguir en el bucle
                        procesoCorrectoBloquue=True

                    if instruccionPosicion == (";") and instruccionPosicion2 == ("}"):
                        procesoCorrecto = False # Para salir del bucle
                        procesoCorrectoBloquue=True
                        return procesoCorrectoBloquue, counter

                    if instruccionPosicion!= (";") and instruccionPosicion2 == ("}"):
                        procesoCorrecto = False #Para salir del bucle
                        procesoCorrectoBloquue = True

                    if instruccionPosicion!= (";") and instruccionPosicion2 != ("}"):
                        procesoCorrecto = False# El proceso esta bien solo que debe salirse del codigo
                        procesoCorrectoBloquue=False

                    if instruccionPosicion==("}"):
                        procesoCorrecto = False
                        procesoCorrectoBloquue=True

            if procesoCorrecto== False and verificacionBloqueCod==False: # Quiere decir que la instruccion estaba mal
                procesoCorrectoBloquue=False
                return procesoCorrectoBloquue, counter

    return procesoCorrectoBloquue,counter



def VerificarCondicionales(filtered_token_generator, counter,NumeroDeInstruccionFija):
    counter+=1
    controlVerificacionCondicionales=False
    instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
    direcciones=["north","south","east","west"]
    if instruccionPosicion==("facing") or("can"):
        condiconal=instruccionPosicion
        counter+=1
        instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
        if condiconal==("facing") or ("can") and (instruccionPosicion==("(")):
            if condiconal==("facing"):
                counter+=1
                instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
                if instruccionPosicion in direcciones:
                    counter += 1
                    instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
                    if instruccionPosicion==(")"):
                        controlVerificacionCondicionales=True
                    else:
                        controlVerificacionCondicionales=False
                else:
                    controlVerificacionCondicionales=False

            if condiconal==("can"):
                counter+=1
                instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija] #La parte del comando
                validarCondicion,counter=validationOpIntern(filtered_token_generator, counter, NumeroDeInstruccionFija, instruccionPosicion)
                if validarCondicion==True: # Counter queda en el parentesis
                    controlVerificacionCondicionales=True
                    counter+=1
                else:
                    controlVerificacionCondicionales=False
        pass

    if instruccionPosicion==("not"):
        counter+=1
        instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
        if instruccionPosicion==(":"):
            counter += 1
            instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
            if instruccionPosicion==("facing") or ("can") or ("not"):
                counter += 1
                putRecursion,counter=VerificarCondicionales(filtered_token_generator, counter,NumeroDeInstruccionFija)
                if putRecursion==True:
                    controlVerificacionCondicionales=True
            else:
                controlVerificacionCondicionales=False

    return controlVerificacionCondicionales,counter


def bloqueCodigo(filtered_token_generator, counter,NumeroDeInstruccionFija,variablesCreadas,corchetesCounter,procesoCorrecto,Words):
    instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
    controlOperacion=False
    validacionOperacionInternal,counter = validationOpIntern(filtered_token_generator, counter, NumeroDeInstruccionFija,instruccionPosicion)

    if validacionOperacionInternal ==True:
        controlOperacion=True
    else:
        controlOperacion=False

    return controlOperacion,counter


def validationOpIntern(filtered_token_generator, counter,NumeroDeInstruccionFija,instruccionPosicion):
    prueba = ["grab", "get", "drop", "letGo"]
    prueba2=["walk",'lead']
    ControlvalidationOpIntern=False
    #TODO ESTAS NO VALIDAN;
    counter+=1
    ControlComas=True
    parentesiss = filtered_token_generator[counter][NumeroDeInstruccionFija]
    if parentesiss == ("("):
        ControlvalidationOpIntern=True
        counter += 1
        parentesisCounter=0

        if instruccionPosicion == ("jump"):  # TIENE 2 PARAMETROS Y 2 SON VALORES
                verificacionNumero, instruccionPosicionNumero = ProcesamientoNumber(filtered_token_generator, counter,NumeroDeInstruccionFija)
                if verificacionNumero == True or instruccionPosicionNumero in variablesCreadas:  # la siguiente instruccion es una coma
                    counter += 1
                    parentesisCounter += 1
                    ControlComas=True
                    ControlComas, parentesisCounter = comaDeterminante(filtered_token_generator, counter, NumeroDeInstruccionFija, ControlComas,parentesisCounter)
                    # Si control Comas es falso quiere decir que encontro una coma si es True es un parentesis
                    if ControlComas == False:  # Verificar siguiente valor y parentesis
                        counter += 1
                        verificacionNumero, instruccionPosicionNumero = ProcesamientoNumber(filtered_token_generator,counter,NumeroDeInstruccionFija)
                        if verificacionNumero == True or instruccionPosicionNumero in variablesCreadas:
                            counter += 1
                            ControlComas, parentesisCounter = comaDeterminante(filtered_token_generator, counter,NumeroDeInstruccionFija, ControlComas,parentesisCounter)
                            if ControlComas == True:  # Instruccion Correcta se queda en el parentesis.
                                ControlvalidationOpIntern = True

                            else:
                                ControlvalidationOpIntern = False
                        else:
                            ControlvalidationOpIntern = False
                    else:
                        ControlvalidationOpIntern = False
                else:
                    ControlvalidationOpIntern = False

        elif instruccionPosicion in prueba2:# HAY 3 WALKS CON ENTRADAS DIFERENTES
            parentesisCounter += 1
            verificacionNumero,instruccionPosicionNumero=ProcesamientoNumber(filtered_token_generator, counter, NumeroDeInstruccionFija)
            if verificacionNumero==True or instruccionPosicionNumero in variablesCreadas :
                counter += 1
                ControlComas,parentesisCounter = comaDeterminante(filtered_token_generator, counter,NumeroDeInstruccionFija, ControlComas,parentesisCounter)
                if ControlComas==True: #ES PARENTESIS
                    ControlvalidationOpIntern = True
                if ControlComas==False: #ES COMA
                    counter += 1
                    instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
                    if instruccionPosicion==("front") or ("right") or ("left") or ("left") or ("north") or ("south") or ("west") or ("east"):
                        counter += 1
                        ControlComas, parentesisCounter = comaDeterminante(filtered_token_generator, counter, NumeroDeInstruccionFija, ControlComas,parentesisCounter)
                        if ControlComas==True: # Es parentesis es decir que ahi termina la insutruccion
                            ControlvalidationOpIntern=True

                        else:
                            ControlvalidationOpIntern=False
                    else:
                        ControlvalidationOpIntern=False
            else:
                ControlvalidationOpIntern=False

        elif instruccionPosicion == ("turn"):  # recibe left o right o  left, right, or around
            parentesisCounter += 1
            instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
            if instruccionPosicion == ("left") or ("right") or ("around"):  # VAMOS BIEN
                ControlComas, parentesisCounter = comaDeterminante(filtered_token_generator, counter,NumeroDeInstruccionFija, ControlComas, parentesisCounter)
                if ControlComas == True:  # Es parentesis es decir que ahi termina la insutruccion
                    ControlvalidationOpIntern = True
                if ControlComas == False or parentesisCounter != 2:
                    ControlvalidationOpIntern = False
            else:
                ControlvalidationOpIntern = False

        elif instruccionPosicion == ("turnto"):# recibe north, south, east or wes
            parentesisCounter += 1
            instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
            if instruccionPosicion == ("north") or ("south") or ("east") or ("west"):  # VAMOS BIEN
                ControlComas, parentesisCounter = comaDeterminante(filtered_token_generator, counter, NumeroDeInstruccionFija, ControlComas,parentesisCounter)
                if ControlComas == True:  # Es parentesis es decir que ahi termina la insutruccion
                    ControlvalidationOpIntern = True
                    return ControlvalidationOpIntern
                if ControlComas == False or parentesisCounter != 2:
                    ControlvalidationOpIntern = False
            else:
                ControlvalidationOpIntern = False
        elif instruccionPosicion in prueba:# recibe valores o variables
            parentesisCounter += 1
            verificacionNumero,instruccionPosicionNumero=ProcesamientoNumber(filtered_token_generator, counter, NumeroDeInstruccionFija)
            if verificacionNumero==True or instruccionPosicionNumero in variablesCreadas:
                counter += 1
                ControlComas=True
                ControlComas, parentesisCounter = comaDeterminante(filtered_token_generator, counter,NumeroDeInstruccionFija, ControlComas,parentesisCounter)
                #Si control Comas es falso quiere decir que encontro una coma si es True es un parentesis
                if ControlComas == True:
                    ControlvalidationOpIntern=True
                else:
                    ControlvalidationOpIntern=False
            else:
                ControlvalidationOpIntern=False
        elif instruccionPosicion == ("nop"): # STRING VACIO
            ControlComas, parentesisCounter = comaDeterminante(filtered_token_generator, counter,NumeroDeInstruccionFija, ControlComas, parentesisCounter)
            if ControlComas==True:
                ControlvalidationOpIntern = True
            else:
                ControlvalidationOpIntern = False

    else:
        ControlvalidationOpIntern=False

    return ControlvalidationOpIntern,counter

def comaDeterminante(filtered_token_generator, counter,NumeroDeInstruccionFija, ControlComas,parentesisCounter):
    instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija]
    if instruccionPosicion == (","):  # En el caso de que la siguiente insutrcciuon sea una coma bien
        ControlComas = False
    if instruccionPosicion == (")"):
        parentesisCounter += 1
        ControlComas = True

    return ControlComas, parentesisCounter

def procesoInternoOperador(filtered_token_generator, counter, NumeroDeInstruccionFija,variablesCreadas,parentesisCounter,procesoCorrecto,ControlComas):

    instruccionPosicion = filtered_token_generator[counter][NumeroDeInstruccionFija] # Aca ya esta en la siiguietne instruccion despues del parentesis

    if ControlComas==False:# Quiere decir que el sigueinte debe ser una Coma o un parentesis
        if instruccionPosicion in variablesCreadas:
            procesoCorrecto=True
        if instruccionPosicion not in variablesCreadas:
            procesoCorrecto=False
        ControlComas=True
    else: #VERIFICAR DESPUES DE LA VARIABLE QUE SEA UNA COMA O UN PARENTESIS
        ControlComas,parentesisCounter=comaDeterminante(filtered_token_generator,counter,NumeroDeInstruccionFija,ControlComas,parentesisCounter)
    return procesoCorrecto,ControlComas,parentesisCounter




filtered_token_generator=[]
filtered_token_generator = Creacion("feliz",filtered_token_generator)
first = filtered_token_generator.pop(0)
Procesamiento=ProcesamientoDatos(filtered_token_generator)
if Procesamiento!= True:
    print("False")
else:
    print("True")
#print(filtered_token_generator)