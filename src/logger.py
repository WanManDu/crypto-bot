import logging
import os

def setup_logger(log_filename='trade.log'):
    """
    로거 설정 함수
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 파일 핸들러
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    
    # 포맷 지정
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # 로거에 핸들러 등록
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
