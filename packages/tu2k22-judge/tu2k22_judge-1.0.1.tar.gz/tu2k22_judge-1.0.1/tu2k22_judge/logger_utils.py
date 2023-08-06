import logging


def get_logger(name: str, level: int = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level=level)
    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def game_visualizer(level: int = logging.INFO):
    logger = logging.getLogger("visualizer")
    logger.setLevel(level=level)
    formatter = logging.Formatter(fmt='%(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
