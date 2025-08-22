import logging
from logging.handlers import RotatingFileHandler
import gzip
import shutil
import os

LOG_DIR = "/var/log/mkdocs-panel"
LOG_FILE = f"{LOG_DIR}/painel.log"

os.makedirs(LOG_DIR, exist_ok=True)

class GZipRotatingFileHandler(RotatingFileHandler):
    def doRollover(self):
        super().doRollover()
        last_log = f"{self.baseFilename}.1"
        if os.path.exists(last_log):
            with open(last_log, 'rb') as f_in:
                with gzip.open(f"{last_log}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(last_log)

def setup_logging():
    logger = logging.getLogger("painel_logger")
    logger.setLevel(logging.INFO)
    handler = GZipRotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logging()

