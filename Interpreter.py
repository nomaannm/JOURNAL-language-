from Tokens import *
class Interpreter:
    def __init__(self, tree, base):
        self.tree = tree
        self.data = base
    


    def read_INT(self,value):
        return int(value) 
    
    def read_FLT(self,value):
        return float(value) 
    
    # to save data and to retrieve data
    def read_VAR(self,id):
        variable = self.data.read(id)
        variable_type = variable.Type
        return getattr(self , f"read_{variable_type}")(variable.value)



    def compute_bin(self,lNode , operator ,rNode):
        lNodetype = "VAR" if str(lNode.Type).startswith("VAR") else str(lNode.Type) # VAR(INT)
        rNodetype = "VAR" if str(rNode.Type).startswith("VAR") else str(rNode.Type)

        if operator.value == "=":
            # say a = 5 -> rNodetype (already computed)
            lNode.Type = f"VAR({rNodetype})"
            self.data.write(lNode,rNode)
            return self.data.read_all()


        lNode = getattr(self , f"read_{lNodetype}")(lNode.value) #read_INT(value)
        rNode = getattr(self, f"read_{rNodetype}")(rNode.value) #read_FLT(value)

        if operator.value == "+":
            output =  lNode + rNode
        elif operator.value == "-":
            output = lNode - rNode
        elif operator.value == "*":
            output = lNode * rNode
        elif operator.value == "/":
            output =  lNode/rNode
        elif operator.value == ">":
            output = 1 if lNode > rNode else 0
        elif operator.value == "<":
            output = 1 if lNode < rNode else 0
        elif operator.value == ">=":
            output = 1 if lNode >= rNode else 0
        elif operator.value == "<=":
            output = 1 if lNode <= rNode else 0
        elif operator.value == "?=":
            output = 1 if lNode == rNode else 0
        elif operator.value == "!=":
            output = 1 if lNode != rNode else 0
        elif operator.value == "and":
            output = 1 if lNode and rNode else 0
        elif operator.value == "or":
            output = 1 if lNode or rNode else 0
        
        #Not is a unary operator we have formed a different operand for that
        # parse.py << LINE 18

        


            # even if one of the numbers would be a float , the whole output would become float 
        return Integer(output) if (lNodetype == 'INT' and rNodetype == 'INT') else Float(output)


    def compute_unary(self,operator,operand):
        operand_type = "VAR" if str(operand.Type).startswith("VAR") else str(operand.Type)
        operand = getattr(self, f"read_{operand_type}")(operand.value)

        
        if operator.value == "+":
            output = +operand
        elif operator.value == "-":
            output = -operand
        elif operator.value == "not":
            output =  1 if not operand else 0
        

        return Integer(output) if (operand_type == "INT") else Float(output)
    def interpret(self , tree = None): 
    #This tree = None method specifies that if the interpret() would not be given any parameter , any error would not occur.

        # this method is responsible for computing our arithmetic 
        # 1 + 2 * 5
        #     +
        #   /  \
        #  1    *
        #      / \
        #     2   5
        # Post order traversal will be used , Left subtree , Right Subtree , Root node
        # 1 + 1 = [1 , + , 1]\

        if tree is None:
            tree = self.tree


        if isinstance(tree ,list):
            if isinstance(tree[0],Reserved):
                if tree[0].value == "if":
                    for self.idx , condition in enumerate(tree[1][0]):
                        evaluation = self.interpret(condition)
                        if evaluation.value == 1:
                            return self.interpret(tree[1][0][self.idx])
                        
                    if len(tree[1]) == 3:
                        return self.interpret(tree[1][2])
                    
                    else:
                        return
                
                elif tree[0].value == "while":
                    print("Entered")
                    condition = self.interpret(tree[1][0])
                    action = self.interpret(tree[1][1])
                    print(condition)
                    print(action)
                    while condition.value == 1:
                        # Doing the action
                        print(self.interpret(tree[1][1]))

                        #checking the condition
                        condition = self.interpret(tree[1][0])
                        print(condition.value)
                    
                    return 

        #UNARY Operation
        if isinstance(tree ,list) and len(tree) == 2:
            expression = tree[1]
            if isinstance(expression ,list):
                expression = self.interpret(expression)
            return self.compute_unary(tree[0],expression)
        
        #No Operation
        elif not isinstance(tree,list):
            return tree
        
        #BINARY Operation
        else:
             left_node = tree[0]
             if isinstance(left_node , list):
                 left_node = self.interpret(left_node)
        
             right_node = tree[2]
             if isinstance(right_node,list):
                right_node = self.interpret(right_node)

             operator = tree[1] # ROOT NODE 

             return self.compute_bin(left_node,operator,right_node)



        

       

# Necessary Info : while traversing , if we encounter a subtree , then typeof(subtree) would be list.