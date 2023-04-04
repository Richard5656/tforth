import sys


if len(sys.argv) == 1:
    print("expected tforth.py [filename]")
    exit(1)

code =  open(sys.argv[1],'r').read().replace("\\n","\n")

"""
: CR 10 EMIT ;
: IF INVERT BC ;
: THEN LBL ;
: ELSE LBL BC ;
: BEGIN LBL ;
: UNTIL BC ;
VARIABLE i
VARIABLE end
: DO ! ! LBL ;
: LOOP
     DUP DUP ( duplicates index VARIABLE )
     @ 1 + SWAP ! ( Increment index )
     @ SWAP @ < ( Compare )
    BC ; ( Branch )
    
90 end 0 i 
DO
    i @ . CR
     end i 
LOOP


VARIABLE vtest
0 vtest !
(
BEGIN
    vtest @ 1 + vtest !
    vtest @ . CR
    vtest @ 10 <
UNTIL
)
"""
stk = [0 for i in range(0,16000)]


tokens = code.upper().replace('\n'," ").replace('\t'," ").replace('\r'," ").strip().split(" ")

for i in range(tokens.count("")):   #remove white space
    tokens.remove("")
def printn(s):
    print(s,end = "")

pc = 0
label_jmp_flag = 0
varible_pointer_counter = 10000
string_pointer_counter = 8000

user_def_word = {}
primative_words = {}
primative_words["."] = lambda : printn(str(stk.pop()))
primative_words["EMIT"] = lambda : printn(chr(stk.pop()))
primative_words["DUP"] = lambda : stk.append(stk[-1]);
primative_words["DROP"] = lambda : stk.pop();



def ADD(): global stk; op1 = stk.pop();op2 = stk.pop();stk.append( op2 + op1)
def SUB(): global stk; op1 = stk.pop();op2 = stk.pop();stk.append( op2 - op1)
def MUL(): global stk; op1 = stk.pop();op2 = stk.pop();stk.append( op2 * op1)
def DIV(): global stk; op1 = stk.pop();op2 = stk.pop();stk.append( op2 / op1)
def LESS(): global stk; op1 = stk.pop();op2 = stk.pop();stk.append( op2 < op1)
def GREATER(): global stk; op1 = stk.pop();op2 = stk.pop();stk.append( op2 > op1)
def EQUAL(): global stk; op1 = stk.pop();op2 = stk.pop();stk.append( op2 == op1)
def AND(): global stk; op1 = stk.pop();op2 = stk.pop();stk.append( op2 & op1)
def OR(): global stk; op1 = stk.pop();op2 = stk.pop();stk.append( op2 | op1)
def XOR(): global stk; op1 = stk.pop();op2 = stk.pop();stk.append( op2 ^ op1)
def INVERT(): global stk; op1 = stk.pop();stk.append( not op1)
def DEREF(): global stk; op1 = stk.pop();stk.append(stk[op1])
def WRITEMEM(): global stk; op1 = stk.pop(); stk[op1]= stk.pop()
def SWAP(): global stk; op1 = stk.pop();op2 = stk.pop();stk.append( op1);stk.append( op2)
def IMPORT():
    global tokens,pc
    tokens_external = open(tokens[pc],'r').read().replace("\\n","\n").upper().replace('\n'," ").replace('\t'," ").replace('\r'," ").strip().split(" ")
    for i in range(0,tokens_external.count("")):   #remove white space
        tokens_external.remove("")
   
    pc-=1
    tokens.pop(pc)
    tokens.pop(pc)
    for i in range(0,len(tokens_external)):
        tokens.insert(pc+i,tokens_external[i])
   

def STRING():
    global string_pointer_counter, tokens,pc, stk
    i = 0
    stk.append(string_pointer_counter)
    while(tokens[pc][i] != '"'):
        stk[string_pointer_counter] = ord(tokens[pc][i])
        string_pointer_counter+=1
        i+=1
    stk.append(len(tokens[pc])-2)
    string_pointer_counter+=1
    pc+=1



def FLPJF(): # flips jump flag forcing program to jump wherever you want
    global label_jmp_flag
    label_jmp_flag ^= 1
   
   
   
def LBL(): global label_jmp_flag; label_jmp_flag = 1

primative_words["IMPORT"] = IMPORT    
primative_words["+"] = ADD
primative_words["-"] = SUB
primative_words["*"] = MUL
primative_words["/"] = DIV
primative_words["<"] = LESS
primative_words[">"] = GREATER
primative_words["="] = EQUAL
primative_words["AND"] = AND
primative_words["OR"] = OR
primative_words["LBL"] = LBL
primative_words["INVERT"] = INVERT
primative_words["@"] = DEREF
primative_words["!"] = WRITEMEM
primative_words["SWAP"] = SWAP
primative_words["S\""] = STRING
primative_words["XOR"] = XOR
primative_words["FLPJF"] = FLPJF


primative_words["STOP"] = lambda : exit(-1)


primative_words["SBLK"] = lambda : 0
primative_words["EBLK"] = lambda : 0



def RKBLK(): # returns to SBLK
    global pc,tokens
    flag_ = 0
    pc-=1
    while(tokens[pc] != "SBLK" or flag_ != 0):
            if(tokens[pc] in user_def_word and
            user_def_word[tokens[pc]]["type"] == "mf" and
            (not (tokens[pc] in user_def_word[tokens[pc]]["exp"])) ): expand_mf() ; pc+=1
            pc-=1
            
            if(tokens[pc] == "EBLK"): flag_ +=1            
            if(tokens[pc] == "SBLK"): flag_ -=1

def SKBLK(): # skips block by Jumping to EBLK
    global pc,tokens
    flag_ = 0
    while(tokens[pc] != "EBLK"or flag_ != 0):
            if(tokens[pc] in user_def_word and
            user_def_word[tokens[pc]]["type"] == "mf" and
            (not (tokens[pc] in user_def_word[tokens[pc]]["exp"])) ):expand_mf() ; pc-=1;
            pc+=1
            if(tokens[pc] == "EBLK"): flag_ -=1
            if(tokens[pc] == "SBLK"): flag_ +=1
def RKBLKC(): # returns to SBLK if condition
    global pc,tokens,label_jmp_flag
    if(stk.pop()):
        RKBLK()
       
       
def SKBLKC(): # skips block by Jumping to EBLK
    global pc,tokens,label_jmp_flag
    if(stk.pop()):
        SKBLK()





def SRKBLK(): # returns to SBLK
    global pc,tokens
    flag_ = 0
    while(tokens[pc] != "SBLK" or flag_ != 0):
            if(tokens[pc] in user_def_word and
            user_def_word[tokens[pc]]["type"] == "mf" and
            (not (tokens[pc] in user_def_word[tokens[pc]]["exp"])) ): expand_mf() ; pc+=1
            pc-=1
            if(tokens[pc] == "EBLK" ): flag_ +=1
            if(tokens[pc] == "SBLK"and flag_ != 0): flag_ -=1
           
def SSKBLK(): # skips block by Jumping to EBLK
    global pc,tokens
    flag_ = 0
    while(tokens[pc] != "EBLK"or flag_ != 0):
            if(tokens[pc] in user_def_word and
            user_def_word[tokens[pc]]["type"] == "mf" and
            (not (tokens[pc] in user_def_word[tokens[pc]]["exp"])) ):expand_mf() ; pc-=1;
            pc+=1
            if(tokens[pc] == "EBLK"and flag_ != 0): flag_ -=1
            if(tokens[pc] == "SBLK" ): flag_ +=1
def SRKBLKC(): # returns to SBLK if condition
    global pc,tokens,label_jmp_flag
    if(stk.pop()):
        SRKBLK()
       
       
def SSKBLKC(): # skips block by Jumping to EBLK
    global pc,tokens,label_jmp_flag
    if(stk.pop()):
        SSKBLK()




primative_words["RKBLK"] = RKBLK
primative_words["SKBLK"] = SKBLK
primative_words["RKBLKC"] = RKBLKC
primative_words["SKBLKC"] = SKBLKC
primative_words["SRKBLK"] = SRKBLK
primative_words["SSKBLK"] = SSKBLK
primative_words["SRKBLKC"] = SRKBLKC
primative_words["SSKBLKC"] = SSKBLKC

def B():
    global pc,tokens,label_jmp_flag
       
   
    if(label_jmp_flag == 1):
        pc-=1
        while(tokens[pc] != "LBL"):
            if(tokens[pc] in user_def_word and
            user_def_word[tokens[pc]]["type"] == "mf" and
            (not (tokens[pc] in user_def_word[tokens[pc]]["exp"])) ):
                expand_mf()
                pc+=1
            pc-=1
        pc+=1
    else:
        pc+=1
        while(tokens[pc] != "LBL"):
            if(tokens[pc] in user_def_word and
            user_def_word[tokens[pc]]["type"] == "mf" and
            (not (tokens[pc] in user_def_word[tokens[pc]]["exp"])) ):
                expand_mf()
                pc-=1
            pc+=1
        pc+=1
primative_words["B"] = B
def BC():
    global pc,tokens,label_jmp_flag
    if(stk.pop()):
        B()
    else:
        label_jmp_flag = 0
primative_words["BC"] = BC


def get_tok():
    global pc
    tok = tokens[pc]
    pc+=1
    return tok


def expand_mf():
    global tokens,pc
    curtok = tokens[pc]
    tokens.pop(pc)
    for i in range(0,len(user_def_word[curtok]["exp"])):
        tokens.insert(pc+i,user_def_word[curtok]["exp"][i])

#eval mode
def eval_forth():
 
    global pc,stk,primative_words,user_def_word,varible_pointer_counter
    while pc < len(tokens):
        curtok = get_tok()
        if curtok in user_def_word:
            if(user_def_word[curtok]["type"] == "mf"): # obsolete macro expander
                pc-=1 # get to name of mf
                expand_mf()
            elif user_def_word[curtok]["type"] == "var":
                stk.append(user_def_word[curtok]["loc"])

        elif curtok.isdigit():
            stk.append(int(curtok))
        elif curtok == ":":
            name = tokens[pc]
            pc+=1 # skip word name
            user_def_word[name] = {"type": "mf", "exp":[]}
            while (tokens[pc] != ';'):
                user_def_word[name]["exp"].append(tokens[pc])
                pc+=1
            pc+=1 # skip ;
        elif curtok == "VARIABLE":
            name = tokens[pc]
            pc+=1 # skip word name
            user_def_word[name] = {"type": "var", "loc":varible_pointer_counter}
            varible_pointer_counter+=1
        elif curtok in primative_words:
            primative_words[curtok]()
        elif curtok == '(':
            while(tokens[pc] != ')'):
                pc+=1
            pc+=1
        elif curtok == ';': # do nothing
            1+1
        else:
            print(f"User word has not been defined yet: {curtok}")
            exit(-1)
eval_forth()
print()
#print(user_def_word)
#print(stk)
#print(tokens)
