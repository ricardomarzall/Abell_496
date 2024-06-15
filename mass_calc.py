from lib import *
from variables import *
from astropy import constants as const
from sympy import gamma

u.def_unit(
    ["kpc", "kiloparsec"],
    1000 * u.pc,
    namespace=globals(),
    prefixes=True,
    doc="Kiloparsec: 1000 parsecs."
)

processor = Temperature_Processor(pkl_temp_path)
processor.Temp_estimator()
temperature = np.array(processor.temperature[:-2])
temperature = np.delete(temperature, 11)
Raio = np.array(RegionProcessor(reg_path).kpc_Radius(redshift)[:-2])
Raio = np.delete(Raio, 11)
mean_errors = np.array(processor.erro[:-2])
mean_errors = np.delete(mean_errors, 11)

processor_2 = RegionProcessor(reg_path)
processor_2.erro_region()
erro_region = np.array(processor_2.list_erro_region[:-2])
erro_region = np.delete(erro_region, 11)
erro_region = (UnitConverter.arcsec_to_kpc(UnitConverter.pixel_to_arcsec(erro_region),0.032))/2

r_profile_fits_path = '/home/vitorfermiano/Documentos/teste_2/surface_brighness.fits'
plotter = Make_surface_brightness_plot(r_profile_fits_path)
plotter.plot_process()

fitter = CurveFitter(Raio, temperature, erro_region, mean_errors)
params, params_covariance = fitter.fit_curve()
fitter.plot_fit()

param_errors = fitter.get_param_errors()

print("Fitted parameters:", params)
print("Parameter errors:", param_errors)
print("aqui", gamma(3*plotter.get_beta() - 0.5))

k = const.k_B.value
G = const.G.to((u.kpc * u.m**2)/(u.kg * u.s**2)).value
mu = 0.6
mp = const.m_p.value
c = params[2]
d = params[3]
beta = (plotter.get_beta())
rc = UnitConverter.arcsec_to_kpc(UnitConverter.pixel_to_arcsec(plotter.get_r0()),0.032)
a  = params[0]
b = params[1]
S0 = plotter.get_ampl()
gamma1 =  np.float64(gamma(3*plotter.get_beta()))
gamma2 = np.float64(gamma(3*plotter.get_beta()-0.5))

# Definindo os valores de R em escala logarítmica
R_values = np.logspace(1, 3, 100)  # Intervalo de R de 0 a 1000 em escala logarítmica

M_values = []
for i in R_values:
    mass_calculator = Mass_Calculator(i, k, G, mu, mp, c, d, beta, rc, a, b, S0, gamma1, gamma2)
    M_values.append((((mass_calculator.calculate_mass())*u.kg).to(u.solMass)).value)

# Calculando M2500
R2500 = 430  # Example value, replace with actual R2500
mass_calculator_2500 = Mass_Calculator(R2500, k, G, mu, mp, c, d, beta, rc, a, b, S0, gamma1, gamma2)
M2500 = (((mass_calculator_2500.calculate_mass())*u.kg).to(u.solMass)).value

print(f"M2500: {M2500:.2e} M_sun")

# Plotando o gráfico em escala logarítmica
plt.figure(figsize=(8, 6))
plt.plot(R_values, M_values, label='Enclosed mass')
plt.axvline(R2500, color='green', linestyle='--', label=f'R2500 = {R2500} kpc')
plt.text(R2500, M2500, f'M2500 = {M2500:.2e} M_sun', verticalalignment='bottom', horizontalalignment='right')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('R (log)',fontsize=25)
plt.ylabel('M (log)',fontsize=25)
#plt.title('Gráfico de M(R) em função de R (escala log-log)')
plt.xticks(fontsize=20)  # Tamanho dos números no eixo X
plt.yticks(fontsize=20)  # Tamanho dos números no eixo Y
# Personalização da legenda
plt.legend(fontsize=20) 
plt.grid(True)
plt.show()


