from xspec import *
import re
import os
import numpy as np
import pickle
#from função_extrair_espectros import extrair_espectros  

def ajuste_apec_xspec(spec_dir,reg_path,AllData,AllModels):
    with open(reg_path, 'r') as file:
        regions = file.readlines()
    print(regions)
    home = os.path.expanduser('~') #pega o home do usuário
    
    temperature = []
    normalização = []
    for i in range(len(regions)):
        spec_file = f"{spec_dir}/spec_espectro_{i}_grp.pi"
        print(2)
        current = os.getcwd()
        os.chdir(spec_dir) # muda o diretorio de trabalho

        try:
            AllData += spec_file
            AllData.ignore("0.0-0.5") 
            AllData.ignore("5.0-7.0")
            AllData.ignore("bad")
            AllModels += "phabs*apec"
            m = AllModels(1) 
            m.phabs.nH = 0.04
            m.phabs.nH.frozen = True
            m.apec.Abundanc=0.4,0.01    
            m.apec.kT= 3.0,0.1
            m.apec.Abundanc.frozen = False
            m.apec.kT.frozen = False 
            m.apec.Redshift = 0.032
            Fit.perform()

            kT_valor_ajustado = m.apec.kT.values[0]
            norm_valor_ajustado = m.apec.norm.values[0]
            print(25)
            Fit.error("1. 2,3,5")
            par2 = AllModels(1)(2) # Temperatura
            par3 = AllModels(1)(3) # Abundância
            par5 = AllModels(1)(5) # Noramlização

            # Erros Temperatura

            kT_erro_1 = par2.error[1]
            kT_erro_0 = par2.error[0]


            kT_erro_positivo = kT_erro_1 - kT_valor_ajustado
            kT_erro_negativo = kT_erro_0 - kT_valor_ajustado

            # Erros normalização
            norm_erro_1 = par5.error[1]
            norm_erro_0 = par5.error[0]
            norm_erro_positivo = norm_erro_1 - norm_valor_ajustado
            norm_erro_negativo = norm_erro_0 - norm_valor_ajustado


            # Listas com os valores dos parâmetros e seus erros
            temperature.append([kT_valor_ajustado, kT_erro_positivo, kT_erro_negativo])
            normalização.append([norm_valor_ajustado,norm_erro_positivo,norm_erro_negativo])
            
            
            AllData.clear()
            AllModels.clear()

        except Exception as e:
            print(f"Error processing {spec_file} in XSPEC: {e}")
            temperature.append([None, None, None])
            normalização.append([None,None,None])
            pass  # Continue para a próxima iteração
    
    temperature = np.array(temperature)
    normalização = np.array(normalização)
    print(temperature)
    print(normalização)
 
    
    diretorio_script = os.path.dirname(__file__)

    # Ao salvar os arquivos
    with open(os.path.join(diretorio_script, 'temp_teste_1.pkl'), 'wb') as arquivo1:
        pickle.dump(temperature, arquivo1)

    with open(os.path.join(diretorio_script, 'normalizacao_teste_1.pkl'), 'wb') as arquivo2:
        pickle.dump(normalização, arquivo2)



spec_dir = '/home/vitorfermiano/Documentos/4976/repro/extract_bin_20_ultimos'
reg_path = '/home/vitorfermiano/Documentos/4976/repro/region.reg'
AllData = AllData
AllModels = AllModels


ajuste_apec_xspec(spec_dir,reg_path,AllData,AllModels)