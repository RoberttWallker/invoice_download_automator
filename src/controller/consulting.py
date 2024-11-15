import sys
from pathlib import Path
from datetime import datetime

ROOT_PATH = Path(__file__).resolve().parent.parent
ROOT_PATH_TESTE = Path.cwd()
print(ROOT_PATH_TESTE)
sys.path.append(str(ROOT_PATH))

from modules.consultas import download_anexos
from modules.metodos import formatar_data, ghost_exec_creation

data_atual = datetime.today().strftime("%d-%b-%Y")
data_inicio = '01-Jan-2024'

# Caminhos dos arquivos .bat e .vbs
bat_file_path = ROOT_PATH / "controller/task_exec_incremental.bat"
vbs_file_path = ROOT_PATH / "controller/ghost_exec_task.vbs"

def download_total():
    while True:
        data = input("Digite a data inicial de busca (dd/mm/aaaa): ")
        try:
            data = formatar_data(data)
            download_anexos(data)
            ghost_exec_creation(bat_file_path, vbs_file_path, ROOT_PATH_TESTE)
            break
        except ValueError as e:
            print(f'\nO formato de data não está correto: {e}\n')


def download_incremental():
    download_anexos(data_atual)