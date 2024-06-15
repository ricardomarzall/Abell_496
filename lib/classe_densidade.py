import pickle
from astropy.cosmology import Planck15
from uncertainties.umath import sqrt
from lib.regions import *
import numpy as np
import matplotlib.pyplot as plt
from lib.converte import *
from astropy import units as u


class Density_Processor:
    def __init__(self, pkl_norm_path):
        self.pkl_norm_path = pkl_norm_path
        self.norm = []
        self.erro = []
        self.densidades = []
            
    def open_file(self):
        '''Abre o arquivo'''
        with open(self.pkl_norm_path, 'rb') as arquivo1:
            norm_carregado = pickle.load(arquivo1)
            return norm_carregado

    def error_estimator(self):  
        norm_carregado = self.open_file()
        error_upper = norm_carregado[:, 1]  # Array - erros superiores
        error_lower = norm_carregado[:, 2]  # Array - erros inferiores
        # Calcula a média dos erros positivos e negativos
        mean_errors = np.mean(np.abs([error_upper, error_lower]), axis=0)
        for i in mean_errors:
            self.erro.append(i)

    def norm_estimator(self):
        norm_carregado = self.open_file()
        self.error_estimator()
        for i in norm_carregado[:, 0]:
            self.norm.append(i)
    
    def calcula_densidade(self, z, mu, N, R_out, R_in):
        cosmo = Planck15
        DA = UnitConverter.mpc_to_cm((cosmo.angular_diameter_distance(z)).value)
        return (10**7) * (1 + z) * DA * sqrt((3 * mu * N) / (R_out**3 - R_in**3))
    
    def density_estimator(self, z, mu):
        self.norm_estimator()
        processor = RegionProcessor('/home/vitorfermiano/Documentos/4976/repro/region.reg')
        processor.make_inner_radius_list()
        processor.make_out_radius_list()
        raio_interno = processor.list_innerradius
        raio_externo = processor.list_outradius
        norm = self.norm
        for i in range(len(norm)):
            N = norm[i]
            R_in = UnitConverter.mpc_to_cm(UnitConverter.arcsec_to_mpc(UnitConverter.pixel_to_arcsec(raio_interno[i]), z))
            R_out = UnitConverter.mpc_to_cm(UnitConverter.arcsec_to_mpc(UnitConverter.pixel_to_arcsec(raio_externo[i]), z))
            self.densidades.append(self.calcula_densidade(z, mu, N, R_out, R_in))



