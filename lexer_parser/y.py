
import tokenize
from io import BytesIO

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

string_proc = tokenize.tokenize(BytesIO("a , u , y , i , o , l".encode('utf-8')).readline)

print(check_token_sequence(string_proc))
