from Tokens import Integer , Float , Operation , Declaration , Variables , Boolean , Comparison , Reserved

# Grammer Rules of the language 
# to declare variables 'say' keyword would be used ,ex : say varName = something !


class Lexer:
    digits = '0123456789'
    letters = 'abcdefghijklmnopqrstuvwxyz_'
    Uletters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_' 
    HindiLetters = 'अआइईउऊऋएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक्षत्रज्ञश्रौैाीूोे्िुॉंॅ'
    operations = '+-*/()='
    varDeclaration = ["say"]
    constDeclaration = ["hook"]
    logDeclaration = ["flush"]
    boolDeclaration = ["boolean"] #this one is for declaring True or False switches in a variable
    boolean = ["and" , "or" , "not" , "nand" , "nor" , "xor" , "xnor"] # this one if for boolean operations
    stopwords = [" "]
    comparsion_operators = [">","<",">=","<=" , "?=" "!="]
    specialCharacters = "><=?!"
    reserved = ["if" , "elseif" , "else" , "do" , "while" , "for"]
    def __init__(self,text):
        self.text = text
        self.idx = 0 
        self.tokens = []
        self.char = self.text[self.idx]
        self.token = None
    
    def tokenize(self):
        while self.idx < len(self.text):
            if self.char in Lexer.digits:
                self.token = self.extract_number()
            
            elif self.char in Lexer.operations:
                self.token = Operation(self.char)
                self.move()

            elif self.char in Lexer.stopwords:
                self.move()
                continue 
            
            elif self.char in Lexer.letters or self.char in Lexer.Uletters:
                word = self.extract_word()
                if word in Lexer.varDeclaration:
                    self.token = Declaration(word)
                
                elif word in Lexer.boolean:
                    self.token = Boolean(word)
                
                elif word in Lexer.reserved:
                    self.token = Reserved(word)

                else:
                    self.token = Variables(word)

            elif self.char in Lexer.specialCharacters:
                comparisonOperator = ""
                while self.char in Lexer.specialCharacters and self.idx < len(self.text):
                    comparisonOperator += self.char
                    self.move()

                self.token = Comparison(comparisonOperator)

            self.tokens.append(self.token)
        return self.tokens

    

    def extract_number(self):
        number = "" #storing the number as a string to iterate over it 
        isFloat = False
        while (self.char in Lexer.digits or self.char == ".") and (self.idx < len(self.text)):
            if self.char == ".":
                isFloat = True
            number += self.char
            self.move()

        return Integer(number) if not isFloat else Float(number)
    
    def extract_word(self):
        word = ""
        while(self.char in Lexer.letters or self.char in Lexer.Uletters) and (self.idx < len(self.text)):
            word += self.char
            self.move()

        return word
            
    
    def move(self):
        self.idx += 1
        if self.idx < len(self.text):
            self.char = self.text[self.idx]


