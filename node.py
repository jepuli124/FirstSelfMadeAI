class node():
    def __init__(self, bias:float):
        self.bias = bias
        self.output = 0
    
    def copy(self):
        return node(self.bias)