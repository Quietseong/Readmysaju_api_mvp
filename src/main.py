import uvicorn
from .api import app

if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",  # 모듈 경로 수정
        host="0.0.0.0",
        port=8001,
        reload=True
    )