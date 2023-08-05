import datetime
import logging
import sys
from pathlib import Path
from typing import Final

LOG_FOLDER: Final[Path] = Path(__file__).parent / "Logs"

if not LOG_FOLDER.exists():
    LOG_FOLDER.mkdir(parents=True)


def _get_log_path(folder: Path = LOG_FOLDER) -> Path:
    current_time = datetime.datetime.now().replace(microsecond=0)
    current_time_str = str(current_time).replace(":", "-")
    return folder / f"{current_time_str}.log"


def add_file_handler():
    fh = logging.FileHandler(_get_log_path())
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


logger = logging.getLogger("fitbit-downloader")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
