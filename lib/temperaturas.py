import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import uncertainties as un
import pickle

from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


class Temperature_Processor:

    def __init__(self,pkl_temp_path):
        self.pkl_temp_path = pkl_temp_path
        self.temperature = []
        self.erro = []
        
    def open_file(self):
        '''Abre o arquivo'''
        with open(self.pkl_temp_path, 'rb') as arquivo1:
            temperature_carregado = pickle.load(arquivo1)
            return temperature_carregado

    def error_estimator(self):  
        temperature_carregado = self.open_file()
        
        error_upper = temperature_carregado[:,1]  # Array - erros superiores
        error_lower = temperature_carregado[:,2]  # Array - erros inferiores
        # Calcula a média dos erros positivos e negativos
         
        mean_errors = np.mean(np.abs([error_upper, error_lower]), axis=0)
        for i in mean_errors:
       
            self.erro.append(i)
    def Temp_estimator(self):
        temperature_carregado = self.open_file()
        self.error_estimator()
        
        for i in temperature_carregado[:,0]:
            self.temperature.append(i)
        
class CurveFitter:
    def __init__(self, radius, temperature, error_radius, error_temperature):
        self.radius = radius
        self.temperature = temperature
        self.error_radius = error_radius
        self.error_temperature = error_temperature

    @staticmethod
    def model_function(R, a, b, c, d):
        return a + b * np.exp(-c * R) - d * R

    def fit_curve(self):
        # Initial guess for the parameters
        initial_guess = [6.503, -4.626, 0.014, 0.002]#[75464226.11512351, -53682532.67854243, 4.536616979909268e-24, 7.520755026681788e-18]

        # Define parameter bounds
        param_bounds = ([-np.inf, -np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf, np.inf])

        # Perform the curve fitting
        params, params_covariance = curve_fit(
            self.model_function, 
            self.radius, 
            self.temperature,
            sigma=self.error_temperature,
            absolute_sigma=True,
            p0=initial_guess,
            bounds=param_bounds,
            maxfev=30000  # Increase max number of function evaluations
        )
        
        self.params = params
        self.params_covariance = params_covariance
        return params, params_covariance

    def plot_fit(self):
        plt.errorbar(self.radius, self.temperature, yerr=self.error_temperature, xerr=self.error_radius, fmt='o', label='Data with errors')
        fitted_temperature = self.model_function(self.radius, *self.params)
        plt.plot(self.radius, fitted_temperature, label='Fitted curve')
        plt.xlabel('Radius (R)',fontsize=20)
        plt.ylabel('Temperature (T)',fontsize=20)
        plt.xticks(fontsize=20)  # Tamanho dos números no eixo X
        plt.yticks(fontsize=20)  # Tamanho dos números no eixo Y
        # Personalização da legenda
        plt.legend(fontsize=20) 
        plt.show()

    def get_param_errors(self):
        param_errors = np.sqrt(np.diag(self.params_covariance))
        return param_errors





