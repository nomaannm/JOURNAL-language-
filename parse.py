# 1 + 2 * 3
# [1 , + , [2 ,*,3]]
class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.idx = 0 
        self.token = self.tokens[self.idx]
    # <factor> := 0,1,2,3,2.3,5.1, (<expr>)........whatever
    # <term> := 1 * 2, 2 * 6 , 1/2 , 5/3 ........ et cetera
    # <expr> := 1 * 2 + 3 * 2,2/3 - 4/3 ....... many more
    def factor(self):
        if self.token.Type == "INT" or self.token.Type == "FLT":
            return self.token
        elif self.token.value == "(":
            self.move()
            expression = self.boolExpression()
            return expression
        elif self.token.value == "not":
            operator = self.token
            self.move()
            return [operator,self.boolExpression()]
        elif self.token.Type.startswith("VAR"): #startswith is an inbuilt method in python
            return self.token
        elif self.token.value == "+" or self.token.value == "-":
            operator = self.token
            self.move()
            operand = self.boolExpression()
            return [operator,operand]

            
        
    def term(self):
        # 1 * 2 : 1 -> LeftNode , * -> RootNode , 2 -> RightNode
        left_node = self.factor()
        self.move()
        output = left_node
        while self.token.value == "*" or self.token.value == "/":
            operation = self.token
            self.move()
            right_node = self.factor()
            self.move()
            left_node = [left_node , operation , right_node]

        return left_node
    
    # Comparison Expression
    def compExpression(self):
        #<comp> := <expr> >|<|?=|!=|<=|>= <expr>
        left_node = self.expression()
        while self.token.Type == "COMPARE" :
            operation = self.token
            self.move()
            right_node = self.expression()
            left_node = [left_node,operation,right_node]
        
        return left_node


    def boolExpression(self):
        # <bool_expr> := <comp_expr> and|or|not|nand|nor|xnor|xor <comp_expr>
        left_node = self.compExpression()
        while self.token.Type == "BOOL":
            boolean_operation = self.token
            self.move()
            right_node = self.compExpression()
            left_node = [left_node , boolean_operation , right_node]

        return left_node


    def expression(self):
        left_node = self.term()
        output = left_node
        while self.token.value == "+" or self.token.value == "-":
            operation = self.token
            self.move()
            right_node = self.term()
            left_node = [left_node , operation , right_node]
        
        return left_node
    def if_statement(self):
        self.move()
        condition = self.boolExpression()

        if self.token.value == "do":
            self.move()
            action = self.statement()

            return condition , action
        
        elif self.tokens[self.idx - 1].value == "do":
            action = self.statement()
            return condition , action
        
    def if_statements(self):
        # if <expr> do <statement> elif <expr> do <statement>....... else do <statement>
        # <expr> ~ condtions , <statement> ~ actions
        conditions = list()
        actions = list()
        ifStatement = self.if_statement()

        conditions.append(ifStatement[0])
        actions.append(ifStatement[1])

        while self.token.value == "elif":
            ifStatement = self.if_statement()
            conditions.append(ifStatement[0])
            actions.append(ifStatement[1])

        if self.token.value == "else":
            self.move()
            self.move()
            else_action = self.statement()

            return [conditions , actions , else_action]
        
        return [conditions , actions]
    
    def while_statement(self):
        self.move()
        condition = self.boolExpression()

        if self.token.value == "do":
            self.move()
            action = self.statement()
            return [condition , action]
        
        elif self.tokens[self.idx-1].value == "do":
            action = self.statement()
            return [condition , action]
    
    def statement(self):
        if self.token.Type == "DECL":
            #variable assignment 
            # say a = 10
            #    =
            #  /  \
            # a    10
            self.move()
            left_node = self.variable()
            self.move()
            if self.token.value == "=":
                operation = self.token
                self.move()
                right_node = self.boolExpression()

            return [left_node , operation , right_node]
        # not 5 ?= 5s
        elif self.token.Type == "INT" or self.token.Type == "FLT" or self.token.Type == "OP" or self.token.value == "not":
            #arithmetic expression
            return self.boolExpression()
        
        elif self.token.value == "if":
            return [self.token , self.if_statements()]
        elif self.token.value == "while":
            return [self.token , self.while_statement()]
        
    

    def variable(self):
        if self.token.Type.startswith("VAR"):
            return self.token


  
    
    def move(self):
        self.idx += 1
        if self.idx < len(self.tokens) :
            self.token = self.tokens[self.idx]

    # we are creating this method for statements like var assignment , loops , conditions etc
   
        

    def parse(self):
        return self.statement()
        
    
   

