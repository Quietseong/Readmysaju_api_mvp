from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from .chat import Chat

app = FastAPI(
    title="ReadMySaju API",
    description="사주 챗봇 API",
    version="1.0.0"
)

# Pydantic 모델 정의
class ChatRequest(BaseModel):
    """채팅 요청 모델"""
    message: str
    tone: Optional[str] = None

class ChatResponse(BaseModel):
    """채팅 응답 모델"""
    response: str
    tone: str

# Chat 인스턴스 생성
chat = Chat()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    채팅 엔드포인트
    
    Args:
        request (ChatRequest): 채팅 요청 데이터
        
    Returns:
        ChatResponse: 채팅 응답 데이터
    """
    try:
        # 톤 변경이 요청된 경우
        if request.tone:
            chat.change_tone(request.tone)
            
        # 쿼리 실행
        response = chat.query(request.message, print_response=False)
        
        return ChatResponse(
            response=response,
            tone=chat.current_tone
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tones")
async def get_tones():
    """
    사용 가능한 톤 목록을 반환하는 엔드포인트
    
    Returns:
        dict: 톤 정보
    """
    return {
        tone_key: {
            "name": tone.name,
            "description": tone.description,
            "characteristics": tone.characteristics,
            "example": tone.example
        }
        for tone_key, tone in chat.tones.items()
    }