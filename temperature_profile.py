import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lib import *
from variables import *

processor = Temperature_Processor(pkl_temp_path)

processor.Temp_estimator()
temperature = processor.temperature
Raio = RegionProcessor(reg_path).kpc_Radius(redshift)
mean_errors = processor.erro

processor_2 = RegionProcessor(reg_path)
processor_2.erro_region()
erro_region = np.array(processor_2.list_erro_region)
erro_region = (UnitConverter.arcsec_to_kpc(UnitConverter.pixel_to_arcsec(erro_region),0.032))/2

# Plotagem do gráfico com barras de erro
plt.errorbar(Raio, temperature, yerr=mean_errors, xerr=erro_region, fmt='.', capsize=3)

# Ajustar o tamanho da fonte dos rótulos dos eixos
plt.xlabel('Radius (kpc)', fontsize=25)
plt.ylabel('Temperatura (keV)', fontsize=25)

# Ajustar o tamanho da fonte das marcas dos eixos
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.xscale("log")
#plt.title('Perfil de Temperatura do Abell 496', fontsize=16)
plt.show()

print(np.mean(temperature))
