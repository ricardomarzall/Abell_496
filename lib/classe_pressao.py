class pressao:
    def __init__(self,density_array,Temperature_array):
        self.density_array = density_array
        self.Temperature_array = Temperature_array
        self.pressure_array = []
    def calcula_pressao(self,density,temperature):
        return 2*density*temperature
    def build_pressure_array(self):
         for i in range(len(self.density_array)):
            self.pressure_array.append(pressao(self.density_array,self.Temperature_array).calcula_pressao(self.density_array[i],self.Temperature_array[i]))
