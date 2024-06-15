from lib import *
from variables import *

#Densidades

processor_3 = Density_Processor(pkl_norm_path)
processor_3.density_estimator(0.032, 1.2)
densidades = processor_3.densidades

# Temperatura

processor = Temperature_Processor(pkl_temp_path)
processor.Temp_estimator()
temperature = processor.temperature


Raio = RegionProcessor(reg_path).kpc_Radius(redshift)
mean_errors = processor.erro

processor_2 = RegionProcessor(reg_path)
processor_2.erro_region()
erro_region = np.array(processor_2.list_erro_region)
erro_region = (UnitConverter.arcsec_to_kpc(UnitConverter.pixel_to_arcsec(erro_region),0.032))/2

Entropy = []

for i in range(len(densidades)):
        Entropy.append(Entropia(densidades[i],temperature[i]).calcula_Entropia())

# Plotagem do gráfico com barras de erro
plt.errorbar(Raio, Entropy, yerr=0,xerr=erro_region, fmt='.', capsize=2) 
plt.xlabel('Raio (kpc)',fontsize=25)
plt.xscale("log")
plt.yscale("log")
plt.ylabel('kev /(cm²)',fontsize=25)
#plt.title('Perfil de Entropia do Abell 496')
plt.show()
