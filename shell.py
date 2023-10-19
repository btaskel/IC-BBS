import logging

def initLogging(level=logging.INFO):
    if level == 5:
        level = logging.DEBUG
    elif level == 4:
        level = logging.INFO
    elif level == 3:
        level = logging.WARNING
    elif level == 2:
        level = logging.ERROR
    elif level == 1:
        level = logging.CRITICAL
    else:
        level = logging.INFO

    logging.basicConfig(
        filename='debug.log',
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y/%m/%d %I:%M:%S '
    )
    logging.debug('debug message')