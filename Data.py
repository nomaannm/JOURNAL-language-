class Data:
    def __init__(self):
        self.variablesDict = dict()

    def read(self,id):
        return self.variablesDict[id]
    
    def read_all(self):
        return self.variablesDict
    
    def write (self , Variables , expression):
        variable_name = Variables.value
        self.variablesDict[variable_name] = expression