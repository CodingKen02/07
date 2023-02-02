#!/usr/bin/env python3
# macroAssembler.py
# macro assembler for hack assembly language
import sys
linecounter=0
parseFileName = ""
linecountList = []
parseFileList = []
parseError = False

# classify line 
class lineType:
    def __init__(self,line):
        # classify line of assembly code
        linesplit1 = line.split()
        # remove comments from line
        linesplit = []
        for i in linesplit1:
            if len(i)>=2 and i[0]=='/' and i[1] =='/':
                break ;
            linesplit.append(i)
            
        #split line by space delimiter
        # by default assume line is a comment
        self.cmdtype="comment"
        self.data=""
        self.arglist=[]
        self.val = -1
        if len(linesplit)>0 and len(linesplit[0]) > 0 :
            if linesplit[0] == '//': #Comment
                self.data = line
            elif len(linesplit[0])>2 and linesplit[0][0]=='/' and linesplit[0][1]=='/':
                self.data = line
            elif linesplit[0] == '$def': # Begining of Macro Definition
                self.cmdtype = "macrodefine"
                self.data = linesplit[0][1:]
                self.arglist = linesplit
            elif linesplit[0] == '$end': # End of Macro Definition
                self.cmdtype = "macroend"
                self.data = linesplit[0][1:]
                self.arglist = linesplit
            elif linesplit[0] == '$include': # include file
                self.cmdtype = "include"
                self.data = linesplit[1]
                self.arglist = linesplit
            elif linesplit[0][0] == '$': # Instantiate Macro
                self.cmdtype="macroinstance"
                self.data = linesplit[0][1:]
                self.arglist = linesplit
            elif linesplit[0][0] == '(': # Symbol definition
                self.cmdtype="symbol"
                slen = len(linesplit[0]) 
                self.data=linesplit[0][1:slen-1]
            elif linesplit[0][0] == '=': # Symbol Assignment
                self.cmdtype="setsymbol"
                if len(linesplit[0]) > 1:
                    self.data = linesplit[0][1:]
                    self.val = convert2int(linesplit[1])
                else:
                    self.data = linesplit[1]
                    self.val = convert2int(linesplit[2])
            elif linesplit[0][0] == '@': # A Instruction
                self.cmdtype="atype"
                self.data=linesplit[0][1:]
            else: # If nothing else then must be C instruction
                self.cmdtype="ctype" 
                self.data=linesplit[0]

# Save information about macro definition
class macroInfo:
    def __init__(self,name,arguments,instructions,symbols):
        # Macro has name, arguments, list of instruction, and internal symbols
        self.name = name
        self.arguments = arguments
        self.instructions = instructions
        self.symbols = symbols

# convert string to int including "0x" definitions for hex numbers and "0b
# for binary numbers
def convert2int(val):
    global parseError
    # For short strings that cant be 0x# or 0b# just convert to integer
    if(len(val) < 3):
        return int(val)
    # Check for hexadecimal encoding
    if val[0]=='0' and val[1]=='x': # hex coding
        sum = 0 
        for i in range(2,len(val)):
            sum=sum*16
            if val[i]>='0' and val[i]<='9':
                sum = sum + (ord(val[i])-ord('0'))
            elif val[i]>='a' and val[i]<='f':
                sum = sum + (ord(val[i])-ord('a')+10)
            elif val[i]>='A' and val[i]<='F':
                sum = sum + (ord(val[i])-ord('A')+10)
            else:
                print("invalid hexidecimal number input", val, "on line", linecounter, "in file" , parseFileName)
                parseError = True
        return sum

    # Check for binary encoding
    if val[0]=='0' and val[1]=='b': # binary coding
        sum = 0
        for i in range(2,len(val)):
            sum = sum*2
            if val[i]=='1':
                sum=sum+1
            elif val[i]!='0':
                print("invalid binary number input",val,"on line",linecounter,"in file", parseFileName)
                parseError = True
        return sum
    # if not hexadecimal or binary, then just use boring decimal conversion
    return int(val)

# convert value to sixteen bit string to output a instructions
def sixteenBitString(val):
    bits = ""
    cnt = 32768
    for j in range(15,-1,-1):
        if val >= cnt:
            bits=bits+'1'
            val =  val - cnt ;
        else:
            bits=bits+'0'
        cnt = cnt/2
    return bits

# this class will save the assembly code for the various passes needed
# to process the symbol tables and then convert the codes into machine
# code when needed
class assemblyCode:
    def __init__(self):
        # list of assembly code to output
        self.code = list()
        # list of machine code to output
        self.machineCode = list()
        # list of all variables assigned static addresses
        self.statics = list()
        # symbol table initialized with default symbols
        self.symbolTable={'R0':0,'R1':1,'R2':2,'R3':3,
            'R4':4,'R5':5,'R6':6,'R7':7,
            'R8':8,'R9':9,'R10':10,'R11':11,
            'R12':12,'R13':13,'R14':14,'R15':15,
            'SP':0,'LCL':1,'ARG':2,'THIS':3,'THAT':4,
            'SCREEN':16384,'KBD':24576 }
        # instruction counter
        self.icount = 0
        # destination register code dictionary
        self.destCodes = {"":"000","A":"100","D":"010","M":"001",
                          "AD":"110","DA":"110","AM":"101","MA":"101",
                          "DM":"011","MD":"011",
                          "ADM":"111","AMD":"111","DAM":"111","DMA":"111",
                          "MAD":"111","MDA":"111"}
        # computation code dictionary
        self.commandCodes = {"0":"0101010","1":"0111111","-1":"0111010",
                             "D":"0001100","A":"0110000","M":"1110000",
                             "!D":"0001101","~D":"0001101",
                             "!A":"0110001","~A":"0110001",
                             "!M":"1110001","~M":"1110001",
                             "-D":"0001111","-A":"0110011","-M":"1110011",
                             "D+1":"0011111","A+1":"0110111","M+1":"1110111",
                             "D-1":"0001110","A-1":"0110010","M-1":"1110010",
                             "D+A":"0000010","D+M":"1000010","D-A":"0010011",
                             "D-M":"1010011","A-D":"0000111","M-D":"1000111",
                             "D&A":"0000000","D&M":"1000000",
                             "A&D":"0000000","M&D":"1000000",
                             "D|A":"0010101","D|M":"1010101",
                             "A|D":"0010101","M|D":"1010101",
                             "JMP":"0101010"}
        # jump code dictionary
        self.jmpCodes={""   :"000","JGT":"001","JEQ":"010","JGE":"011",
                       "JLT":"100","JNE":"101","JLE":"110","JMP":"111"}

    #convert C instruction into binary code
    def translateCode(self,instruction):
        global parseError
        global parseFileName
        global linecounter 
        indx = 0
        # these are the destination register bits
        dest = "000"
        # destination register will be either A, M, or D presented in
        # that specific order
        for i in range(0,min(4,len(instruction))):
            if instruction[i] == '=':
                indx = i
                break
        if indx > 0:
            destcmd = instruction[0:indx]
            if destcmd in self.destCodes:
                dest = self.destCodes[destcmd]
            else:
                print("invalid destination ", destcmd, "on line" ,linecounter, "in file", parseFileName)
                parseError = True 
            
        if instruction[indx] == '=':
            # Recorded destination, now interpret computation
            indx=indx+1
        else:
            # No assignment, so reinterpret string as computation
            indx= 0
            dest="000"
        #parse out the computation instruction into cmd
        cmd=""
        loc = indx
        for i in range(indx,len(instruction)):
            if instruction[i] == ';':
                break
            cmd = cmd + instruction[i]
            loc = loc+1
        # set the computation bits according to the specified computation
        acbits = "0101010"
        if cmd in self.commandCodes:
            acbits = self.commandCodes[cmd]
        else:
            print("UNDEFINED computation instruction, ", instruction, "line" ,linecounter,"in file", parseFileName)
            parseError = True 

        # now interpret jump instruction
        if cmd=="JMP":
            jmp = cmd
        else:
            indx=loc
            #if a ';' still exists in string, skip it
            if indx<len(instruction) and instruction[indx] == ';':
                indx=indx+1

            #copy the jump code to jmp
            jmp=""
            for i in range(indx,len(instruction)):
                jmp=jmp+instruction[i]
        jbits="000"
        if jmp in self.jmpCodes:
            jbits = self.jmpCodes[jmp]
        else:
            print("unable to interpret jump code ",jmp, "on line", linecounter,"in file", parseFileName)
            parseError = True
        # Having interpreted all the components of the c-instruction
        # we now compose the bits into a 16 bit machine code
        bits = "111"+acbits+dest+jbits
        return bits

    #insert a C instruction into the list
    def insertCInstruction(self,instruction):
        # add C instruction to assembly code
        self.code.append(instruction)
        # translate C instruction to binary code
        mcode = self.translateCode(instruction)
        # add binary code to machine code
        self.machineCode.append(mcode)
        # count translated instructions (for assigning symbols
        self.icount = self.icount + 1

    #insert an A instruction into the list (with symbols)
    def insertAInstruction(self,instruction):
        # for an A instruction defer symbolic lookup until later
        # and @ instruction to both assembly and machine code
        modifier = "@"+instruction
        self.machineCode.append(modifier)
        self.code.append(modifier)
        # A instructions increase instruction count
        self.icount = self.icount + 1

    # insert symbol definition into the instruction stream
    def insertSymbol(self,symbol):
        global parseError
        # symbols get inserted into assembly output only
        modifier = "("+symbol+")"
        self.code.append(modifier)
        # Add current address to symbol table
        if symbol in self.symbolTable:
            print("repeated definition of symble ", symbol, "on line", linecounter,"in file", parseFileName)
            parseError = True
        self.symbolTable[symbol] = self.icount

    # insert special symbol assign instruction into the instruction stream
    def insertSymbolAssign(self,symbol,val):
        global parseError
        modifier = "=" + symbol + " " + str(val)
        self.code.append(modifier) ;
        if symbol in self.symbolTable:
            print("repeated definition of symble ", symbol, "on line", linecounter,"in file", parseFileName)
            parseError = True
        self.symbolTable[symbol] = val
        
    # save the assembly code into an asm file (Useful for checking the
    # macro mechanism.  Note this asm file may not work with the
    # nand2tetris assembler if special features are utilized
    def writeAsmCode(self,file):
        # write out assembly code to filename in "file"
        outfile = open(file,'w')
        for i in self.code:
            outfile.write(i+"\n")
        outfile.close()

    # write out the hack file that matches the instructions
    def writeMachineCode(self,file):
        #write out machine code to filename in "file"
        # convert symbols on A instructions when writing file.
        outfile = open(file,"w")
        varbase = 16
        for i in self.machineCode:
            if i[0]=='@':
                data = i[1:len(i)]
                if len(data)> 0 and data[0] >= '0' and data[0] <= '9':
                    Aval = convert2int(data)
                    if Aval >=32769:
                        print("A instruction value to large, val=",Aval)
                else:
                    if data in self.symbolTable:
                        Aval = self.symbolTable[data]
                    else:
                        if len(data)>0 and data[0] == '-':
                            print("invalid symbol, ", data) ;
                        Aval = varbase
                        varbase = varbase+1
                        self.statics.append(data)
                        self.symbolTable[data] = Aval
                Aval = Aval & 0x7fff
                outstring = sixteenBitString(Aval)
                outfile.write(outstring+"\n")
            else:
                outfile.write(i+"\n")
        outfile.close()
            
# replace a macro call with the assembly code that defines the macro
def instantiateMacro(macroname,instance,arglist):
    global macrocounter
    global linecounter
    global parseFileName
    global parseError
    if not (macroname in macrotable):
        print("WARNING, macro",macroname, "not found! line:", linecounter,"file:",parseFileName)
        parseError = True
        return
    instancename = macroname + str(instance)
    localsymbols = dict()
    localsymbols[macroname] = instancename
    marglist = macrotable[macroname].arguments ;
    if len(marglist) != len(arglist)-1:
        print("ERROR: macro ", macroname, " incorrect number of arguments!, line:",linecounter,"file:",parseFileName)
        parseError=True
        return
    for i in range(0,len(marglist)):
        localsymbols[marglist[i]] = arglist[i+1] 
    for i in macrotable[macroname].symbols:
        localsymbols[i] = instancename+"."+i

    for i in macrotable[macroname].instructions:
        if i.cmdtype == "symbol":
            localsymbols[i.data] = instancename + "." + i.data
    
    for i in macrotable[macroname].instructions:
        if i.cmdtype == "atype":
            if i.data in localsymbols:
                outputcode.insertAInstruction(localsymbols[i.data])
            else:
                outputcode.insertAInstruction(i.data)
        elif i.cmdtype == "ctype":
            outputcode.insertCInstruction(i.data) ;
        elif i.cmdtype == "symbol":
            if i.data in localsymbols:
                outputcode.insertSymbol(localsymbols[i.data])
            else:
                outputcode.insertSymbol(i.data)
        elif i.cmdtype == "setsymbol":
            outputcode.insertSymbolAssign(i.data,i.val)
            
        elif i.cmdtype == "macroinstance":
            if i.data in macrotable:
                macrocounter = macrocounter + 1
                instantiateMacro(i.data,macrocounter-1,i.arglist)
            else:
                print("UNDEFINED MACRO INSTANCE: ",i.data,"line:",linecounter,"file:",parseFileName)
                parseError = True 

# parse the input assembly file and build a table of macros and the
# output assembly code
def parseFile(filename,macrotable,outputcode):
    global linecounter
    global parseFileName
    global linecountList
    global parseFileList
    global parseError
    linecountList.append(linecounter)
    parseFileList.append(parseFileName)
    parseFileName = filename
    linecounter=0
    global macrocounter
    infile = open(filename,'r')
    a = True
    while a:
        linein = infile.readline()
        linecounter=linecounter+1
        if not linein:
            a = False
        else:
            #decode line
            decode = lineType(linein)
            #based on instruction type, generate output code
            if decode.cmdtype == "macrodefine":
                b = True
                macroname = decode.arglist[1]
                macroargs = decode.arglist[2:]

                instructions=[]
                symbols=set()
                while b:
                    linein = infile.readline() ;
                    linecounter=linecounter+1
                    if not linein:
                        b=False
                        a=False
                    else:
                        #process macro
                        decodem = lineType(linein)
                        if decodem.cmdtype == "macroend":
                            b=False
                        elif decodem.cmdtype == "ctype":
                            instructions.append(decodem)
                        elif decodem.cmdtype=="atype":
                            instructions.append(decodem)
                        elif decodem.cmdtype=="macroinstance":
                            instructions.append(decodem)
                        elif decodem.cmdtype=="symbol":
                            instructions.append(decodem)
                            symbols.add(decodem.data)
                        elif decodem.cmdtype!="comment":
                            print("unexpected command while parsing macro definition, line:",linecounter,"file:",parseFileName)
                            parseError = True 
                            
                macrotable[macroname] = macroInfo(macroname,macroargs,instructions,symbols)
            elif decode.cmdtype == "macroinstance":
                if decode.data in macrotable:
                    macrocounter = macrocounter + 1
                    instantiateMacro(decode.data,macrocounter-1,decode.arglist)
                else:
                    print("UNDEFINED MACRO INSTANCE: ",decode.data, "line:",linecounter,"File:",parseFileName)
                    parseError = True 
                    outputcode.insertAInstruction("FAILEDMACRO")
            elif decode.cmdtype == "include":
                parseFile(decode.data,macrotable,outputcode)
            elif decode.cmdtype == "atype":
                outputcode.insertAInstruction(decode.data)
            elif decode.cmdtype == "ctype":
                outputcode.insertCInstruction(decode.data)
            elif decode.cmdtype == "symbol":
                outputcode.insertSymbol(decode.data)
            elif decode.cmdtype == "setsymbol":
                outputcode.insertSymbolAssign(decode.data,decode.val)
            elif decode.cmdtype != "comment":
                print("Unexpected input, line:", linecounter, "file:", parseFileName)
                parseError = True
    infile.close()
    linecounter = linecountList.pop()
    parseFileName = parseFileList.pop()

file="input"
if len(sys.argv) > 1:
    file = sys.argv[1]
ifilename = file+".masm"
ofilename = file+".pasm"
hfilename = file+".hack"

print(f'Input File:{ifilename:10} OutputFile:{hfilename:10}')

infile = open(ifilename,'r')


# where we save our macros
macrotable = dict() 


# count macro instance counter
macrocounter=0

outputcode = assemblyCode()

parseFile(ifilename,macrotable,outputcode)

if parseError:
    print("Errors in parsing", ifilename , "  ASSEMBLY ABORTED!")
    exit(-1)
outputcode.writeAsmCode(ofilename)
outputcode.writeMachineCode(hfilename)

# We are finished  so write out some information about the assembled code
print("Defined",len(macrotable), "macros, instantiated",macrocounter)
print("Defined ", len(outputcode.symbolTable),"symbols.")
print("Assembled", outputcode.icount, "instructions.")
if len(outputcode.statics)>0:
    print("static variables identified=",outputcode.statics) 
print(outputcode.symbolTable)

        
