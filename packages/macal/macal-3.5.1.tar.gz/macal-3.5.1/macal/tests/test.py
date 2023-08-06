# History:
#
# 3.5.1 25-05-2022: Changed header to only include history for this file, removed all old history.
#

import macal
import sys


def TryStrToInt(value: str) -> int:
	try:
		return int(value)
	except Exception as ex:
		print(ex)
		return -1

def loadFile(filename):
	with open (filename, mode = 'r', encoding = 'utf-8') as text_file:
		source = text_file.read()
	return source

testno = 3
testLexer = False
testParser = False

if len(sys.argv) > 0:
	if sys.argv[1] == 'lexer':
		filename = './lexer_test.mcl'
		testLexer = True
	elif sys.argv[1] == 'parser':
		filename = './lexer_test.mcl'
		testParser = True
	else:		
		testno = TryStrToInt(sys.argv[1])
		if testno < 0:
			testno = 3
		filename = f"./test{testno}.mcl"

if testLexer:
	source = loadFile(filename)
	lexer = macal.MacalTokenizer()
	tokens = lexer.lex(source, filename)
	for token in tokens:
		#print(token.location, " ", token.token_value if not token.token_type == macal.LexTokenTypes.Comment else "Comment.")
		print(token)
elif testParser:
	source = loadFile(filename)
	lexer = macal.MacalTokenizer()
	tokens = lexer.lex(source, filename)
	parser = macal.MacalParser()
	AST = parser.parse(tokens, filename)
	print(AST)
else:
	lang = macal.Macal()
	try:
		lang.run_from_file(filename)
	except macal.LexError as ex:
		print(ex)
	except macal.SyntaxError as ex:
		print(ex)
	except macal.RuntimeError as ex:
		print(ex)
	#except Exception as ex:
	#	print(f'Unhandled: {ex}')