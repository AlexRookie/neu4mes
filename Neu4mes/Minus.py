import Neu4mes

class Minus(Neu4mes.Relation):
    def __init__(self, obj = None):
        if obj is None:
            return
        super().__init__(obj.json)
        obj_name = obj.name
        self.name = obj.name+'_minus'
        self.json['Relations'][self.name] = {
            'Minus':[obj_name]
        }

def createMinus(self, name, input):
    return -input

setattr(Neu4mes.Neu4mes, 'Minus', createMinus)