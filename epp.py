import os, sys

inInte = False
variables = {}

def lexer(e):
	tokens = []
	types = ['str', 'num', 'bool', 'setting']
	operators = {"+": "ADD", "-": "SUBTRACT", "*": "MULTIPLY", "/":"DIVIDE", "^": "POWER"}
	tok = ""
	lFVN = False
	lFES = False
	lFVV = False
	lFCP = False
	jFLV = False
	jFDT = False
	wFPS = False
	iS = False
	iN = False
	cM = False
	string = ""
	tmp = ""
	pVN = ""
	digits = ['0','1','2','3','4','5','6','7','8','9','.']
	tokens.append("SOF")
	for char in e:
		tok += char
		tmp.upper()
		if tok == "%" or tok[-1:] == "%":
			if cM:
				cM = False
			else:
				cM = True
		if cM != True:
			if tok == "exit()" and inInte == True:
				exit("You asked for it.")
				tok = ""
			elif tok == "var":
				tokens.append("VAR")
				tok = ""
			elif tok in types:
				tokens.append(f"TYPE {tok.upper()}")
				jFDT = True
				tok = ""
			elif tok == " " or tok[-1:] == " " or tok == "\n" or tok[-1:] == "\n":
				if iS == True:
					string+=tok
				elif jFDT == True:
					lFVN = True
					jFDT = False
				elif lFVN == True:
					lFVN = False
					tokens.append(f"NAME: {tmp}")
					tmp = ""
					lFES = True
				elif iN == True:
					iN = False
					tokens.append(f"NUMBER: {tmp}")
					tmp = ""
				tok = ""
			elif tok == "'" or tok == '"':
				if iS == False:
					iS = True
					tok = ""
				elif iS == True:
					if wFPS == True:
						wFPS = False
					iS = False
					tokens.append(f"STRING: {string}")
					string = ""
					tok = ""
			elif tok == "=":
				if lFES == True:
					lFES = False
					tokens.append("EQUALS")
					tok = ""
			elif tok in digits:
				if iN == True:
					tmp += tok
				elif iN == False:
					iN = True
					tmp += tok
				tok = ""
			elif tok == "true" or tok == "false":
				tokens.append(f"BOOL: {tok.upper()}")
				tok = ""
			elif tok == "~" or tok[-1:] == '~':
				if iN == True:
					iN = False
					tokens.append(f"NUMBER: {tmp}")
					tmp = ""
					tok = ""
			elif tok == "log(":
				lFCP = True
				wFPS = True
				tokens.append("PRINT")
				tok = ""
			elif tok == ")" and lFCP:
				if wFPS == True:
					tokens.append(f"REFERENCE: {pVN}")
					pVN = ""
					wFPS = False
				lFCP = False
				tokens.append("CLOSE")
				tok = ""
			elif tok[-1:] == "#":
				tokens.append(f'REFERENCE: {tok[:-1]}')
				tok = ""
			elif tok in operators:
				tokens.append(operators[tok])
			else:
				if iS == True:
					string+=tok
					tok = ""
				elif lFVN == True:
					tmp += tok
					tok = ""
				elif wFPS == True:
					if iS != True:
						pVN += tok
					tok = ""
				elif iN == True:
					iN = False
					tokens.append(f"NUMBER: {tmp}")
					tmp = ""
					tok = ""
				else:
					pass
	if iN == True:
		iN = False
	tokens.append("EOF")
	print(tokens)
	return tokens
				
def parser(toks):
	i = 0
	v = 0
	types = ['STR','NUM','BOOL']
	operators = ("ADD","SUBTRACT","MULTIPLY","DIVIDE","POWER")
	wFS = False
	wFN = False
	wFB = False
	lFN = True
	tmp = None
	name = ""
	while i < len(toks):
		try:
			# print(toks[i])
			if toks[i] != "EOF":
				if f"{toks[i]} {toks[i+1][0:6]}" == "PRINT STRING" and toks[i+2] == "CLOSE":
					print(toks[i+1][8:])
				elif f"{toks[i]} {toks[i+1][0:9]}" == "PRINT REFERENCE" and toks[i+2] == "CLOSE":
					ref = toks[i+1][11:]
					if ref in variables:
						print(variables[ref])
					else:
						print(ref)
				elif f"{toks[i]} {toks[i+1][0:4]}" == "VAR TYPE":
					if toks[i+1][5:] in types:
						ty = toks[i+1][5:]
						if ty == types[0]:
							wFS = True
						elif ty == types[1]:
							wFN = True
						elif ty == types[2]:
							wFB = True
					lFN = True
				elif toks[i][0:4] == "NAME":
					name = toks[i][6:]
					lFN = False
				elif toks[i][0:6] == "STRING" and wFS:
					variables[name] = toks[i][8:]
					wFS = False
					name=""
				elif toks[i][0:6] == "NUMBER" and wFN:
					variables[name] = float(toks[i][8:])
					wFN = False
					name=""
				elif toks[i][0:4] == "BOOL" and wFB:
					variables[name] = toks[i][6:]
					wFB = False
					name = ""
				elif toks[i+1] in operators:
					if toks[i][11:] in variables:
						a = variables[toks[i][11:]]
					else:
						a = float(toks[i][8:])
					if toks[i+2][11:] in variables:
						b = variables[toks[i+2][11:]]
					else:
						b = float(toks[i+2][8:])
					if toks[i+1] == "ADD":
						print(a+b)
					elif toks[i+1] == "SUBTRACT":
						print(a-b)
					elif toks[i+1] == "MULTIPLY":
						print(a*b)
					elif toks[i+1] == "DIVIDE":
						print(a/b)
					elif toks[i+1] == "POWER":
						e = a
						f = b
						print(pow(e,f))
				else:
					pass
			i+=1
		except ValueError:
			exit("You probably used a variable you don't have. You're poop.")


def interperator():
	inInte = True
	while True:
		e = str(input("E++ >> "))
		a = lexer(e)
		b = parser(a)
		print(variables)

def epp(fil = None):
	if not fil:
		interperator()
	else:
		try:
			e = open(fil, 'r').read()
			a = lexer(e)
			b = parser(a)
		except:
			exit("File not found. Maybe you missed the extension or mispelled the name?")

if __name__ == "__main__":
	if len(sys.argv) == 2:
		epp(sys.argv[1])
	else:
		epp()
