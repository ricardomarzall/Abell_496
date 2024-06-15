import numpy as np
import uncertainties as un
from astropy.cosmology import Planck15

class UnitConverter:
    @staticmethod
    def mpc_to_cm(Mpc):
        return Mpc * (3.086 * 10**24)
    @staticmethod
    def kpc_to_cm(kpc):
        return kpc * 3.086 * (10**21)

    @staticmethod
    def keV_to_K(keV):
        return keV * (1.1605 * 10**7)

    @staticmethod
    def pixel_to_arcsec(pixel):
        return pixel * 0.492

    @staticmethod
    def arcsec_to_mpc(angular_size_arcsec, redshift, H0=70.0, Omega_M=0.3, Omega_Lambda=0.7):
        # Convert angular size to radians
        angular_size_rad = np.radians(angular_size_arcsec / 3600.0)
        
        # Create an array of redshift values from 0 to the given redshift
        redshift_values = np.linspace(0, redshift, 1000)

        # Calculate the comoving distance in megaparsecs using the trapezoidal rule
        c = 3.0e5  # Speed of light in km/s
        D_Mpc = (Planck15.angular_diameter_distance(redshift)).value
        
        # Calculate the physical size in megaparsecs
        size_mpc = D_Mpc * angular_size_rad 
        return size_mpc

    @staticmethod
    def arcsec_to_kpc(angular_size_arcsec, redshift, H0=70.0, Omega_M=0.3, Omega_Lambda=0.7):
        size_mpc = UnitConverter.arcsec_to_mpc(angular_size_arcsec, redshift, H0, Omega_M, Omega_Lambda)
        size_kpc = size_mpc * 1e3  # Convert Mpc to kpc
        return size_kpc
    
    @staticmethod
    def arcsec_to_pixel(arcsec):
        return arcsec / 0.492



print(UnitConverter.arcsec_to_mpc(100,0.597))



'''

# Exemplo de uso dos métodos de conversão

# Converter Pixel para Arcsec
pixel_value = un.ufloat(37.266, 0.531006)
arcsec_value = UnitConverter.pixel_to_arcsec(pixel_value)
print(f"{pixel_value} pixels é igual a {arcsec_value} arcsec")

# Converter Arcsec para kpc
arcsec_value = 39.9391
redshift = 0.032
kpc_value = UnitConverter.arcsec_to_kpc(arcsec_value, redshift)
print(f"{arcsec_value} arcsec é igual a {kpc_value} kpc")

# Converter Mpc para cm
mpc_value = 3  # exemplo de valor em Mpc
cm_value = UnitConverter.mpc_to_cm(mpc_value)
print(f"{mpc_value} Mpc é igual a {cm_value} cm")

# Converter keV para Kelvin
keV_value = 5  # exemplo de valor em keV
K_value = UnitConverter.keV_to_K(keV_value)
print(f"{keV_value} keV é igual a {K_value} K")

'''