from lib import *
from astropy import constants as const
from variables import *

#Densidades

processor_3 = Density_Processor(pkl_norm_path)
processor_3.density_estimator(0.032, 1.2)
densidades = processor_3.densidades

# Temperatura

processor = Temperature_Processor(pkl_temp_path)
processor.Temp_estimator()
temperature = processor.temperature

# Regiões

Raio = RegionProcessor(reg_path).kpc_Radius(redshift)
mean_errors = processor.erro

processor_2 = RegionProcessor(reg_path)
processor_2.erro_region()
erro_region = np.array(processor_2.list_erro_region)
erro_region = (UnitConverter.arcsec_to_kpc(UnitConverter.pixel_to_arcsec(erro_region),0.032))/2

# Pressões

processor_4 = pressao(densidades,temperature)
processor_4.build_pressure_array()
pressure_array = processor_4.pressure_array


# Plotagem do gráfico com barras de erro
plt.errorbar(Raio, pressure_array, yerr=0,xerr=erro_region, fmt='.', capsize=2) # Não coloquei a propagação de erro em y ainda
plt.xlabel('Raio (kpc)',fontsize=25)
plt.xscale("log")
plt.yscale("log")
plt.ylabel('pressão (kev) / (cm³)',fontsize=25)
#plt.title('Perfil de pressão do Abell 496')
plt.show()
