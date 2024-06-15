
import matplotlib.pyplot as plt
from variables import *
from lib import *
import numpy as np

processor = Density_Processor(pkl_norm_path)
processor.density_estimator(0.032, 1.2)
Raio = RegionProcessor(reg_path).kpc_Radius(redshift)

processor_2 = RegionProcessor(reg_path)
processor_2.erro_region()
erro_region = np.array(processor_2.list_erro_region)
erro_region = (UnitConverter.arcsec_to_kpc(UnitConverter.pixel_to_arcsec(erro_region),0.032))/2
densidades = processor.densidades

print(erro_region)
# Plotagem do gráfico com barras de erro
plt.errorbar(Raio, processor.densidades, yerr=0,xerr=erro_region, fmt='.', capsize=3)
plt.xlabel('kpc')
plt.xscale("log")
plt.yscale("log")
plt.ylabel('densidade')
plt.title('Perfil de Densidade do Abell 496')
plt.show()

