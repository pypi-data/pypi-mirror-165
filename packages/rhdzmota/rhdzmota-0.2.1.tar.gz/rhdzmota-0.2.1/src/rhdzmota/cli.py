import datetime as dt
from typing import Optional

from .settings import logger_manager


logger = logger_manager.get_logger(name=__name__)


class CLI:

    def __init__(self):
        logger.info("CLI Instance created.")
        self.start = dt.datetime.utcnow()

    def hello(self, world: Optional[str] = None):
        logger.debug("CLI Hello command execution.")
        world = world or "world"
        return f"Hello, {world}!"
