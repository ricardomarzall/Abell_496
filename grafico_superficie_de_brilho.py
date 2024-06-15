from lib.superficie_de_brilho import *
from sherpa.astro.data import Data1D
from sherpa.astro.models import Beta1D 
from sherpa.fit import Fit
import matplotlib.pyplot as plt
import astropy.io.fits as fits
import numpy as np
from sherpa.plot import DataPlot, ModelPlot
import uncertainties as un
from lib import *


## Example usage
#conda_ciao_env_path = '/home/vitorfermiano/anaconda3/envs/ciao-4.16'
#fits_file_path = '/home/vitorfermiano/Documentos/4976/repro/4976_c7_clean.fits'
#reg_file_path = '/home/vitorfermiano/Documentos/4976/repro/region.reg'
#output_directory = '/home/vitorfermiano/Documentos/teste_2'
#bkg_file_path = '/home/vitorfermiano/Documentos/4976/repro/bkg_c7_clean.fits'
#
## Create an instance of the class and run the make_rprofile method
#Create_rprofile(conda_ciao_env_path, fits_file_path, reg_file_path, output_directory, bkg_file_path).make_rprofile()

# Load data from FITS file

r_profile_fits_path = '/home/vitorfermiano/Documentos/teste_2/surface_brighness.fits'
plotter = Make_surface_brightness_plot(r_profile_fits_path)
plotter.plot_process()
# Getting the fitted parameters
r0 = plotter.get_r0()
ampl = plotter.get_ampl()
beta = plotter.get_beta()
print(f"Fitted r0: {r0}")
print(f"Fitted amplitude: {ampl}")
print(f"Fitted beta: {beta}")
plotter.surface_brightness_plot()



