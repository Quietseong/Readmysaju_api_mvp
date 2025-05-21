# ReadMySaju_chat

사주 챗봇 프로젝트입니다. OpenAI API, FastAPI, Gradio를 활용하여 사주 해석 및 대화를 제공합니다.

## 프로젝트 구조
```
ReadMySaju_chat/
├── src/                  # 소스 코드 디렉토리
│   ├── __init__.py       # src 패키지 초기화 파일
│   ├── chat.py           # Chat 클래스 (핵심 로직)
│   ├── api.py            # FastAPI 애플리케이션
│   └── main.py           # Uvicorn 서버 실행 스크립트
│   └── test_api_validation.py # API 테스트 스크립트
├── data/                 # 데이터 디렉토리
│   └── system_prompt.json
├── notebooks/            # Jupyter 노트북 디렉토리
│   └── base.ipynb        # 초기 개발 및 Gradio 테스트용 노트북
├── .env.example          # 환경 변수 예시 파일
├── .gitignore            # Git 무시 파일
├── README.md             # 프로젝트 설명
└── requirements.txt      # Python 의존성 파일
```

## 설치 방법

### 1. 저장소 클론
```bash
git clone https://your-repository-url/ReadMySaju_chat.git
cd ReadMySaju_chat
```

### 2. 가상환경 생성 및 활성화 (권장)
```bash
python -m venv .venv
# Windows
.\\.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

## 환경 변수 설정
1. `.env.example` 파일을 참고하여 프로젝트 루트에 `.env` 파일을 생성합니다.
2. 본인의 OpenAI API 키를 입력합니다.

```env
OPENAI_API_KEY=your_openai_api_key_here
```

> ⚠️ `.env` 파일은 절대 커밋하지 마세요! (이미 .gitignore에 포함되어 있습니다)

## 사용 방법

### FastAPI 서버 실행
API 서버를 실행합니다:
```bash
python -m src.main
```
서버가 시작되면 `http://localhost:8001` (또는 `src/main.py`에 설정된 포트)에서 API를 사용할 수 있습니다.
API 문서는 다음 경로에서 확인할 수 있습니다:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

### API 테스트 스크립트 실행
API가 정상적으로 작동하는지 테스트 스크립트를 통해 확인할 수 있습니다 (API 서버가 실행 중이어야 합니다):
```bash
python -m src.test_api_validation
```

### Jupyter 노트북 및 Gradio
- 초기 개발 과정 및 `Chat` 클래스의 테스트, 간단한 Gradio UI는 `notebooks/base.ipynb` 파일에서 확인할 수 있습니다.
- `notebooks/base.ipynb` 내의 Gradio 코드를 실행하면 웹 UI를 통해 챗봇과 상호작용할 수 있습니다. (노트북 환경에서 실행)

## 예시 코드 (OpenAI API 키 설정)
```python
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# ... (애플리케이션 코드)
```

## 라이선스
MIT License 