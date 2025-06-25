from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Word(BaseModel):
    text: str
    topic: str
    created_at: datetime = datetime.now()
    last_reviewed: Optional[datetime] = None
    review_count: int = 0

class Topic(BaseModel):
    name: str
    words: List[Word] = []
