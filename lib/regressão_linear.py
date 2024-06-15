import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from lib.converte import *
from lib.temperaturas import *
from lib.regions import *

#Converter o Raio para cm

Raio_cm = []
for i in Raio:
    Raio_cm.append(converte_Mpc_cm(arcsec_to_Mpc(i)))

Raio_cm = np.array(Raio_cm)    
print(Raio_cm)

erro = (error_upper + np.abs(error_lower)) / 2

#Aqui vou retirar as 10 ultimas lihas de todos os arrays

temperature_2 = temperature[:-10]
erro_2 = erro[:-10]
Raio_cm_2= Raio[:-10] #Raio esta em arcsec

# Dados
x = np.array(Raio_cm_2)
y = np.array(temperature_2)
erro_2 = np.array(erro_2)

# Adicionando uma constante para a regressão linear
X = sm.add_constant(x)

# Ajuste linear ponderado - Considerei o erro como peso para encontrar um ajuster mais apropriado

modelo = sm.WLS(y, X, weights=1/(erro_2**2))
resultado = modelo.fit()

# Imprimir os resultados
print(resultado.summary())


# O coeficiente angular é dado em keV/arcsec, por isso é necessário fazer a conversão para keV/cm

coeficiente_angular = resultado.params[1]/(converte_Mpc_cm(1)*arcsec_to_Mpc(1))
coeficiente_linear = resultado.params[0]

erros_parametros = resultado.bse
erro_coeficiente_angular = erros_parametros[1]
erro_coeficiente_linear = erros_parametros[0]



