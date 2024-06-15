import subprocess
import os

# Para utilizar essa função precisa estar no ambiente virtual do CIAO - "conda activate ciao"

def extrair_espectros(diretorio_trabalho, reg_path, input_file, background_file, extract_folder_name):

    # Caminho para o ambiente Conda do CIAO
    conda_env_path = '/home/vitorfermiano/anaconda3/envs/ciao-4.16'
    #CALDB_path = '/home/rick/caldb_certo'
    
    # Defina a variável de ambiente CALDB
    #os.environ['CALDB'] = CALDB_path

    # Abra o arquivo .reg e leia as regiões
    with open(reg_path, 'r') as file:
        regions = file.readlines()

    # Crie a pasta "extract" no diretório de trabalho
    extract_dir = os.path.join(diretorio_trabalho, extract_folder_name)
    os.makedirs(extract_dir, exist_ok=True)
    
    # Loop sobre as regiões e execute o specextract para cada uma
    for i in range(len(regions)):
        region = regions[i].strip()  # Remova possíveis espaços em branco no início/fim da linha
        outroot = f'espectro_{i}'  # Gere um nome de arquivo de saída

        # Caminho completo para os arquivos de entrada e saída
        input_path = os.path.join(diretorio_trabalho, input_file)
        output_path = os.path.join(extract_dir, f'spec_{outroot}')

        # Comando specextract
        specextract_command = f'{conda_env_path}/bin/specextract "{input_path}[sky={region}]" {output_path} bkgfile="{diretorio_trabalho}/{background_file}[sky={region}]" bkgresp=no binspec=20 mode=h clobber=yes'

        # Execute o comando specextract
        subprocess.run(specextract_command, shell=True, check=True)



diretorio_trabalho = '/home/vitorfermiano/Documentos/4976/repro'
reg_path = '/home/vitorfermiano/Documentos/4976/repro/region.reg'
input_file = '4976_c7_clean.fits'
background_file = 'bkg_c7_clean.fits'
extract_folder_name = 'extract_bin_20_ultimos'


extrair_espectros(diretorio_trabalho, reg_path, input_file, background_file, extract_folder_name)
