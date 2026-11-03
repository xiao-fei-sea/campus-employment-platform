from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class MessageResponse(BaseModel):
    id: int
    title: str
    content: str
    type: str
    is_read: bool
    related_id: Optional[int] = None
    related_type: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class MessageListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: List[MessageResponse]
