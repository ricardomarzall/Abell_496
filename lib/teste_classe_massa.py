import sympy as sp
import numpy as np
from scipy.special import gamma
from lib.converte import *
from astropy import units as u
class Mass_Calculator:
    def __init__(self,R,k,G,mu,mp,c,d,beta,rc,a,b,S0,gamma1,gamma2):
        # Definindo os símbolos
        self.R, self.k, self.G, self.mu, self.mp, self.c, self.d, self.beta, self.rc, self.a, self.b,self.S0, self.gamma_1,self.gamma_2 = R, k, G, mu, mp, c, d, beta, rc, a, b,S0,gamma1,gamma2
        self.M_R = self.calculate_mass()

    # densidade do núcleo
    def calcula_n0(self,cooling_function):
        try:           
            # Perform the calculation
            result = np.sqrt((self.S0 / (np.sqrt(np.pi) * UnitConverter.kpc_to_cm(self.rc)  * cooling_function)) * (self.gamma_1 / self.gamma_2))
            return result
        except TypeError as e:
            print(f"TypeError: {e}")
    
    def calculate_mass(self):
        # Definindo a função de temperatura T(R)
        T_R = (self.a + self.b * np.exp(-self.c * self.R) - self.d * self.R) * 11604525.00617

        cooling_function = 1e-23 * np.sqrt(T_R)
        
        # Definindo a função de densidade n(R)
        n_R = self.calcula_n0(cooling_function) * (1 + (self.R / self.rc)**2)**(-3 * self.beta / 2)
        
        # Definindo a função da massa M(R)
        M_R = (self.k / (self.G * self.mu * self.mp)) * (self.R**2 * (self.b * self.c * np.exp(-self.c * self.R) + self.d) + (3 * self.R * T_R) / 2)
        return M_R
    
    def set_parameters(self, params):
        # Configurar os parâmetros da equação
        self.params = params
    
    def calculate(self, R_value):
        # Substituir os valores de R e outros parâmetros na equação
        M_R_value = self.M_R.subs(self.params).subs(self.R, R_value)
        return M_R_value.evalf()
    
    def calculate_array(self, R_values):
        # Calcular a massa para uma matriz de valores de R
        M_values = []
        for R_value in R_values:
            M_value = self.calculate(R_value)
            M_values.append(M_value)
        return np.array(M_values)
    





'''

# Criando uma instância da classe e definindo os parâmetros
mass_calculator = Mass_Calculator()
params = {
    'k': const.k_B.value, # Substitua pelo valor real
    'G': const.G.value, # Constante gravitacional
    'mu': 1.2, # Substitua pelo valor real
    'mp': 1.6726219e-27, # Massa do próton
    'c': params[2], # Valor da tabela
    'd': params[3], # Valor da tabela
    'beta': 1, # Substitua pelo valor real
    'cooling_function': 1, # Substitua pelo valor real
    'rc': 1, # Substitua pelo valor real
    'a': params[0], # Valor da tabela
    'b': params[1], # Valor da tabela
}
mass_calculator.set_parameters(params)

# Definindo os valores de R em escala logarítmica
R_values = np.logspace(0, 3, 100)  # Intervalo de R de 0 a 1000 em escala logarítmica

# Calculando a massa para uma matriz de valores de R
M_values = mass_calculator.calculate_array(R_values)


print(M_values)

## Plotando o gráfico em escala logarítmica
#plt.figure(figsize=(8, 6))
#plt.plot(R_values, M_values)
#plt.xscale('log')
#plt.yscale('log')
#plt.xlabel('R (log)')
#plt.ylabel('M (log)')
#plt.title('Gráfico de M(R) em função de R (escala log-log)')
#plt.grid(True)
#plt.show()
'''


