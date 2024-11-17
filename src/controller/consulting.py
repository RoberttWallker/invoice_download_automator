import sys
from pathlib import Path
from datetime import datetime


# Insere o diretório src no sys.path para poder fazer as importações corretamente
ROOT_PATH = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_PATH))

# Pasta raiz de trabalho do aplicativo
PATH_WORK = Path.cwd()


# Importações dos módulos após inserir src no sys.path
from modules.consultas import download_anexos
from modules.metodos import formatar_data, ghost_exec_creation

# Formato de data aceito pelo 
data_atual = datetime.today().strftime("%d-%b-%Y")

# Caminhos dos arquivos .bat e .vbs
bat_file_path = ROOT_PATH / "controller/task_exec_incremental.bat"
vbs_file_path = ROOT_PATH / "controller/ghost_exec_task.vbs"

def download_total():
    while True:
        data = input("Digite a data inicial de busca (dd/mm/aaaa): ")
        try:
            data = formatar_data(data)
            download_anexos(data)
            ghost_exec_creation(bat_file_path, vbs_file_path, PATH_WORK)
            break
        except ValueError as e:
            print(f'\nO formato de data não está correto: {e}\n')

def download_incremental():
    download_anexos(data_atual)
