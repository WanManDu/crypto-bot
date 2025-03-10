# Crypto Bot Project

## 프로젝트 개요
- Binance Testnet을 활용한 간단한 트레이딩 봇 프로젝트
- 시세 데이터 수집, 지표 계산, 간단한 매매 전략 및 백테스트 등

## 폴더 구조
- `src/` : 주요 소스 코드
- `notebook/` : Jupyter Notebook 파일
- `.env` : API 키 등 민감정보
- `requirements.txt` : 필요한 라이브러리 목록

## 실행 방법
 가상환경 생성 및 활성화
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux


## `src/config.py`

```python
import os
from dotenv import load_dotenv
import os

# 현재 파일 위치(= src 디렉토리) 기준으로 상위 폴더의 .env를 찾도록 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, '..', '.env')

load_dotenv(dotenv_path=ENV_PATH)

API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
SECRET_KEY = os.getenv("BINANCE_TESTNET_SECRET_KEY")

# 필요한 경우, 거래 심볼, 타임프레임 등 설정도 여기에 넣을 수 있음
DEFAULT_SYMBOL = "BTC/USDT"
DEFAULT_TIMEFRAME = "5m"