from consulting import download_incremental
from pathlib import Path
import logging

ROOT_PATH = Path(__file__).resolve().parent.parent

LOG_DIR = ROOT_PATH / "logs/application_logs"
LOG_FILE = LOG_DIR / "general_logs.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)


if __name__ == "__main__":
    logging.info("Atualização incremental inciada.")
    try:
        download_incremental()
    except Exception as e:
        print(e)
        logging.error(f"Ocorreu um erro durante a carga incremental: {e}")
    logging.info("Atualização incremental encerrada.")