from .GeneralCalculation import Calculation

class Divide3(Calculation):

    def __init__(self, numberNew=1, resultado=0):
        self.newNumber = numberNew
        self.resultado = resultado
        Calculation.__init__(self, self.divideNumber(), 0)
    
    def divideNumber(self):    
        self.resultado = self.newNumber / 3
        return self.resultado

    def __repr__(self):                 
        return "NEW NUMBER {}, resultado {}".format(self.newNumber, self.resultado)

