import logging
import os

def setup_logger(log_filename='trade.log'):
    """
    logger를 세팅하여 반환
    콘솔 출력과 파일 출력을 동시에 수행
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    #이미 핸들러가 등록되어 있지 않은 경우에만 추가
    if not logger.handlers:
        file_handler = logging.FileHandler(log_filename)
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger