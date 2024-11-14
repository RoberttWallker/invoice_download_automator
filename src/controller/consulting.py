import sys
from pathlib import Path
from datetime import datetime

ROOT_PATH = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_PATH))

from modules.consultas import download_anexos

data_atual = datetime.today().strftime("%d-%b-%Y")
data_inicio = '01-Jan-2024'

def download_total():
    download_anexos(data_inicio)

def download_incremental():
    download_anexos(data_atual)