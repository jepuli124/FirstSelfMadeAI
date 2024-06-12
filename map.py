class map():
    def __init__(self, elements):
        self.size = (len(elements), len(elements[0]))
        self.objects = elements
            
    def getX(self, x):
        return self.objects[x]
    
    


