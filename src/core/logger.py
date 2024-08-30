import logging

# from rich.logging import RichHandler
from loguru import logger


logger = logging.getLogger(__name__)

handler = logger()

# logger.setLevel(logging.DEBUG)
# handler.setLevel(logging.DEBUG)

handler.setFormatter(logging.Formatter("%(message)s"))

logger.addHandler(handler)
