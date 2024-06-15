
from lib import *
from variables import *
from astropy import units as u


#Densidades

processor_3 = Density_Processor(pkl_norm_path)
processor_3.density_estimator(0.032, 1.2)
densidades = processor_3.densidades
for idx in range(len(densidades)):
    densidades[idx] = densidades[idx] 

# Temperatura

processor = Temperature_Processor(pkl_temp_path)
processor.Temp_estimator()
temperature = processor.temperature
for idx in range(len(temperature)):
    temperature[idx] = temperature[idx] 

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



# cooling time

processor_5 = cooling_time(densidades,pressure_array,cooling_function)
processor_5.build_cooling_time_array()
cooling_time_array = processor_5.cooling_time_array


print(cooling_time_array)
print(Raio)

# Seus dados e plotagem existentes
plt.errorbar(Raio, cooling_time_array, yerr=0, xerr=2.52, fmt='.', capsize=2)
plt.axvspan(148.35822575161933, 160.3635342964005, color='gray', alpha=0.5, label=r'$R_{cool}$ = 154 kpc ')
plt.axhline(y=14599382329.73071, color='g', linestyle='-', label=r'$H_t$ = 14.599 Gyr ')
plt.xlabel('Raio (kpc)', fontsize=25)
plt.ylabel('cooling time (yr)', fontsize=25)


# Personalização dos eixos
plt.xticks(fontsize=20)  # Tamanho dos números no eixo X
plt.yticks(fontsize=20)  # Tamanho dos números no eixo Y
# Personalização da legenda
plt.legend(fontsize=25)  # Ajusta o tamanho da fonte da legenda para 'large'

# Mostrar o gráfico
plt.show()