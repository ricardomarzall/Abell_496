class Entropia:
    def __init__(self,densidade,Temperatura):
        self.densidade = densidade
        self.Temperatura = Temperatura

    def calcula_Entropia(self): 
        return self.Temperatura*(self.densidade**(-2/3))