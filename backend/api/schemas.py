from pydantic import BaseModel
from typing import List, Optional, Dict


class ChatRequest(BaseModel):
    question: str
    chat_history: Optional[List[Dict[str, str]]] = []


class ChatResponse(BaseModel):
    answer: str
    steps: Optional[List[str]] = []
