from pydantic import BaseModel
from typing import Optional, Any

class BaseResponse(BaseModel):
    status_code: int  # 1=Success, 2=Error
    message: str
    data: Optional[Any] = None
