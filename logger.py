from loguru import logger


logger.add('log_files/debug.log', level='DEBUG', rotation='00:00',compression='zip', enqueue=True, diagnose=True,
           retention="7 days")
