from .GeneralCalculation import Calculation

class Multiply3(Calculation):

    def __init__(self, numberNew=0,resultado=0):
        self.newNumber = numberNew
        self.resultado = resultado
        Calculation.__init__(self, self.multiplyNumber(), 0)
    
    def multiplyNumber(self):
        self.resultado = self.newNumber * 3
        return self.resultado
    
    def __repr__(self):
        return "Multiply NEW NUMBER {}, resultado {}".format(self.newNumber, self.resultado)

