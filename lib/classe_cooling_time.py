class cooling_time:
    def __init__(self, array_density, array_pressure, cooling_function):
        self.array_pressure = array_pressure
        self.array_density = array_density 
        self.cooling_function = cooling_function
        self.cooling_time_array = []

    def calcula_cooling_time(self, density, pressure): 
        return 3 * 3.17098e-8 * pressure*1.60218e-9 / (2 * (density)**2 * self.cooling_function)
    
    def build_cooling_time_array(self):
        for i in range(len(self.array_pressure)):
            self.cooling_time_array.append( self.calcula_cooling_time(self.array_density[i], self.array_pressure[i]))

