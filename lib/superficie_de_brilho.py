import os
import subprocess
#from lib.superficie_de_brilho import *
from sherpa.astro.data import Data1D
from sherpa.astro.models import Beta1D 
from sherpa.fit import Fit
import matplotlib.pyplot as plt
import astropy.io.fits as fits
import numpy as np
from sherpa.plot import DataPlot, ModelPlot
import uncertainties as un
#from lib import *

class Create_rprofile:
    """
    Class to create a radial brightness profile from FITS files using the CIAO dmextract command.

    Attributes:
    ----------
    conda_ciao_env_path : str
        Path to the conda environment where CIAO is installed.
    fits_file : str
        Path to the input FITS file.
    reg_file : str
        Path to the region file.
    bkg_file : str, optional
        Path to the background FITS file. Default is None.
    output_directory : str
        Directory where the output file will be saved.
    """

    def __init__(self, conda_ciao_env_path, fits_file_path, reg_file_path, output_directory, bkg_file_path=None):
        """
        Initializes the Create_rprofile class with the paths of the necessary files and directories.

        Parameters:
        -----------
        conda_ciao_env_path : str
            Path to the conda environment where CIAO is installed.
        fits_file_path : str
            Path to the input FITS file.
        reg_file_path : str
            Path to the region file.
        output_directory : str
            Directory where the output file will be saved.
        bkg_file_path : str, optional
            Path to the background FITS file. Default is None.
        """
        self.conda_ciao_env_path = conda_ciao_env_path
        self.fits_file = fits_file_path 
        self.reg_file = reg_file_path
        self.bkg_file = bkg_file_path
        self.output_directory = output_directory
    
    def make_rprofile(self):
        """
        Creates the radial brightness profile by executing the dmextract command with the provided parameters.

        If a background file is provided, it will be used in the dmextract command.
        """
        # Create the output directory if it doesn't exist
        os.makedirs(self.output_directory, exist_ok=True)
        
        # Check if the provided files and directories exist
        assert os.path.exists(self.conda_ciao_env_path), "Conda environment path not found."
        assert os.path.exists(self.fits_file), "FITS file not found."
        assert os.path.exists(self.reg_file), "Region file not found."
        if self.bkg_file:
            assert os.path.exists(self.bkg_file), "Background file not found."

        # Construct the dmextract command with or without the background file
        if self.bkg_file:
            dmextract_command = (
                f'{self.conda_ciao_env_path}/bin/dmextract '
                f'infile="{self.fits_file}[bin sky=@{self.reg_file}]" '
                f'outfile={os.path.join(self.output_directory, "surface_brighness.fits")} '
                f'bkg="{self.bkg_file}[bin sky=@{self.reg_file}]" '
                'opt=generic clobber=yes'
            )
        else:
            dmextract_command = (
                f'{self.conda_ciao_env_path}/bin/dmextract '
                f'infile="{self.fits_file}[bin sky=@{self.reg_file}]" '
                f'outfile={os.path.join(self.output_directory, "surface_brighness.fits")} '
                'opt=generic clobber=yes'
            )
        
        # Print the command for debugging purposes
        print("Running command:", dmextract_command)
        # Execute the command
        subprocess.run(dmextract_command, shell=True, check=True)


class Make_surface_brightness_plot:
    """
    Class to process and plot surface brightness data from a FITS file using a Beta1D model.

    Attributes:
    ----------
    r_profile_fits_path : str
        Path to the radial profile FITS file.
    r0_val : float
        Fitted parameter r0 of the Beta1D model.
    beta_val : float
        Fitted parameter beta of the Beta1D model.
    ampl_val : float
        Fitted parameter ampl of the Beta1D model.
    x : numpy.ndarray
        Array of Rmid values from the FITS file.
    y : numpy.ndarray
        Array of surface brightness values from the FITS file.
    y_err : numpy.ndarray
        Array of surface brightness errors from the FITS file.
    model : numpy.ndarray
        Fitted model values.
    errors : object
        Errors from the fit.
    """

    def __init__(self, r_profile_fits_path):
        self.r_profile_fits_path = r_profile_fits_path
        self.r0_val = 0
        self.beta_val = 0
        self.ampl_val = 0
        self.x = None
        self.y = None
        self.y_err = None
        self.model = None
        self.errors = None

    def plot_process(self):
        """
        Processes the FITS file and fits a Beta1D model to the data.
        """
        # Open the FITS file and extract data
        hdulist = fits.open(self.r_profile_fits_path)
        data_table = hdulist[1].data

        # Extract data columns
        self.x = data_table['RMID']
        self.y = data_table['SUR_BRI']
        self.y_err = data_table['SUR_BRI_ERR']

        # Check for zero uncertainties and replace with a small non-zero value
        y_err_nonzero = np.where(self.y_err == 0, 1e-10, self.y_err)

        # Create Data1D object with errors
        data = Data1D('name', self.x, self.y, staterror=y_err_nonzero)

        # Create Beta1D model
        src = Beta1D()
        src.r0 = 105
        src.beta = 4
        src.ampl = 0.00993448

        # Freeze the xpos parameter
        src.xpos.frozen = True

        # Create fitting object and fit the model
        fit = Fit(data, src)
        results = fit.fit()

        # Get fitted parameter values
        self.r0_val = src.r0.val
        self.beta_val = src.beta.val
        self.ampl_val = src.ampl.val

        # Create a model with the fitted parameters
        self.model = src(self.x)

        # Estimate errors
        self.errors = fit.est_errors()

    def surface_brightness_plot(self):
        """
        Plots the surface brightness data and the fitted model.
        """
        # Check if plot_process has been called
        if self.x is None or self.model is None:
            raise RuntimeError("Call plot_process() before surface_brightness_plot()")

        # Plotting the data and the model
        plt.figure()
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("R_mid (pixel)")
        plt.ylabel("SB (photons/cm²/pixel²/s)")
        plt.scatter(self.x, self.y, label='Data')
        plt.plot(self.x, self.model, label='Fitted Model', color='red')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_r0(self):
        """
        Returns the fitted r0 value.
        
        Returns:
        --------
        float
            The fitted r0 value.
        """
        return self.r0_val

    def get_ampl(self):
        """
        Returns the fitted amplitude value.
        
        Returns:
        --------
        float
            The fitted amplitude value.
        """
        return self.ampl_val

    def get_beta(self):
        """
        Returns the fitted beta value.
        
        Returns:
        --------
        float
            The fitted beta value.
        """
        return self.beta_val

# Example usage

'''
r_profile_fits_path = '/home/vitorfermiano/Documentos/teste_2/output.fits'
plotter = Make_surface_brightness_plot(r_profile_fits_path)
plotter.plot_process()
plotter.surface_brightness_plot()

# Getting the fitted parameters
r0 = plotter.get_r0()
ampl = plotter.get_ampl()
beta = plotter.get_beta()

print(f"Fitted r0: {r0}")
print(f"Fitted amplitude: {ampl}")
print(f"Fitted beta: {beta}")
'''