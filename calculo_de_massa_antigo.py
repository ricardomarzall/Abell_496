import numpy as np
from lib.temperaturas import * # perfil de temperatura
from astropy import units as u
from astropy import constants as const
from scipy.special import gamma
import pandas as pd
from lib.regions import *   # df.raio - raio em arcmin
from lib.converte import *
from lib.regressão_linear import *
import uncertainties as un
from lib.gamma_function import gamma_with_uncertainty
from uncertainties.umath import sqrt
from lib.superficie_de_brilho import *


# Cooling Function 
# T em Kelvin

def cooling_function(T):
    return 1.4 * (10**(-27)) * sqrt(T) #* u.erg * ((u.cm)**3)/u.s).value n

# densidade do núcleo
def calcula_n0(S0,rc,T,beta):
    return sqrt((S0/(np.sqrt(np.pi)*rc*cooling_function(T)))*(gamma_with_uncertainty(3*beta)/gamma_with_uncertainty(3*beta-0.5)))

# densidade em função de r
def calcula_n(r,S0,rc,beta,T):
    return calcula_n0(S0,rc,T,beta)*((1+(r/rc)**2)**(((-3)* beta)/2))

# derivada da densidade
def derivada_n(r,S0,rc,beta,T):
    return -3*beta*calcula_n0(S0,rc,T,beta)*(rc**(3*beta))*r*(rc**2+r**2)**((-3*beta-2)/2)
    
# Essa função calcula a Temperatura baseado na regressão linear ou temperatura estabilizada(T_flat) 
def calcula_T(r,rmax,derivada_T,constante_temperatura,T_flat): # Essa equação devolve em Kelvin
    if r < rmax:
        return converte_keV_to_K(derivada_T * r + constante_temperatura)  # Converter de keV --> Kelvin
    else:
        return converte_keV_to_K(T_flat) # Converter de keV -> Kelvin


# Função que calcula a massa do aglomerado
# T em K
# r em cm 
   
def Massa(r,rmax,rc,beta,S0,derivada_T,constante_temperatura,T_flat):
    
    k = ((const.k_B).to(u.erg/u.K)).value #Boltzmann Constant erg/K
    G = ((const.G).to(u.cm**3 / (u.g * u.s**2))).value # Constante gravitacional 
    mH = (const.m_p*1000).value # Massa do hidrogênio g
    nu = 0.6 # fator massa reduzida átomo de hidorgenio
    
    #Massa da parte Central em que T < T_flat

    Massa_core = (-k*calcula_T(rmax,rmax,derivada_T,constante_temperatura,T_flat)/(G*nu*mH)) * rmax * (((rmax)/calcula_n(rmax,S0,rc,beta,calcula_T(rmax,rmax,derivada_T,constante_temperatura,T_flat))) * (derivada_n(rmax,S0,rc,beta,calcula_T(rmax,rmax,derivada_T,constante_temperatura,T_flat))) + (rmax/calcula_T(rmax,rmax,derivada_T,constante_temperatura,T_flat)) * derivada_T)
    
    #Massa 1 é a massa sem a derivada da temperatura de forma que englobe toda a região

    Massa_1 = (-k*calcula_T(r,rmax,derivada_T,constante_temperatura,T_flat)/(G*nu*mH)) * r * ((r)/calcula_n(r,S0,rc,beta,calcula_T(r,rmax,derivada_T,constante_temperatura,T_flat))) * (derivada_n(r,S0,rc,beta,calcula_T(r,rmax,derivada_T,constante_temperatura,T_flat)))
    
    #Massa 2 é a massa retirando o core desse calculo com a derivada=0

    Massa_2 = Massa_1 - (-k*calcula_T(rmax,rmax,derivada_T,constante_temperatura,T_flat)/(G*nu*mH)) * rmax * ((rmax)/calcula_n(rmax,S0,rc,beta,calcula_T(rmax,rmax,derivada_T,constante_temperatura,T_flat))) * (derivada_n(rmax,S0,rc,beta,calcula_T(rmax,rmax,derivada_T,constante_temperatura,T_flat)))
    
    #Agora juntando a massa do core(leva em conta a derivada da temperatura) e a massa da região periférica

    Massa_total = Massa_2 + Massa_core
    return Massa_total

erros_parametros = resultado.bse


#Esses parâmetros são definidos pela regrassão linear - regressão_linear.py

derivada_T = un.ufloat(resultado.params[1]/(converte_Mpc_cm(1)*arcsec_to_Mpc(1)),erros_parametros[1]/(converte_Mpc_cm(1)*arcsec_to_Mpc(1))) 
constante_temperatura = un.ufloat(resultado.params[0],erros_parametros[0])


# Parâmetros definidos pela superfície de brilho - superficie_de_brilho.py 
 
rc = converte_Mpc_cm(arcsec_to_Mpc(converte_pixel_arcsec(r0)))


#
rmax = converte_Mpc_cm(0.1) # o raio máximo é o raio em que a temperatura fica estável
r = converte_Mpc_cm(0.43) #Raio do aglomerado


Massa_final = Massa(r,rmax,rc,beta,S0,derivada_T,constante_temperatura,T_flat)

#Convertendo o valor e erro de grama para massa solares 

parte_masssa_final = (((Massa_final.nominal_value)*u.g).to(u.M_sun)).value

erro_massa_final = (((Massa_final.std_dev)*u.g).to(u.M_sun)).value

# Massa toral do Aglomerado

Massa_final = un.ufloat(parte_masssa_final,erro_massa_final)

print(Massa_final)




