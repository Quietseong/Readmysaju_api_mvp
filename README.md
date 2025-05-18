# ReadMySaju_chat

사주 챗봇 프로젝트입니다. OpenAI API와 Gradio를 활용하여 사주 해석 및 대화를 제공합니다.

## 프로젝트 구조
```
ReadMySaju_chat/
├── .env.example           # 환경 변수 예시 파일
├── .gitignore            # Git 무시 파일
├── README.md             # 프로젝트 설명
├── requirements.txt      # pip 의존성 파일
├── pyproject.toml        # Poetry 설정 파일
├── data/                 # 데이터 디렉토리
│   └── system_prompt.json
├── src/                  # 소스 코드 디렉토리
│   └── chat.py
└── notebooks/            # Jupyter 노트북 디렉토리
    └── base.ipynb
```

## 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/ReadMySaju_chat.git
cd ReadMySaju_chat
```

### 2. 가상환경 생성 및 활성화 (선택)
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. 의존성 설치
#### pip 사용 시
```bash
pip install -r requirements.txt
```
#### Poetry 사용 시
```bash
poetry install
```

## 환경 변수 설정
1. `.env.example` 파일을 참고하여 프로젝트 루트에 `.env` 파일을 생성합니다.
2. 본인의 OpenAI API 키를 입력합니다.

```
OPENAI_API_KEY=your_openai_api_key_here
```

> ⚠️ `.env` 파일은 절대 커밋하지 마세요! (이미 .gitignore에 포함되어 있습니다)

## 사용 방법
- Jupyter 노트북(`notebooks/base.ipynb`)에서 예제 실행
- Gradio UI 실행 예시:
```bash
python src/chat.py
```

## 예시 코드
```python
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# ...
```

## 라이선스
MIT License 