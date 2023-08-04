from Lexer import Lexer
from parse import Parser
from Interpreter import Interpreter
from Data import Data

base = Data()

while True:
    text = input("JOURNAL : ")
    tokenizer = Lexer(text)
    tokens = tokenizer.tokenize()
    #print(tokens)
    
    parser = Parser(tokens)
    tree = parser.parse()
    #print(tree)

    interpreter = Interpreter(tree,base)
    result = interpreter.interpret()
    if result is not None:
        print(result)