from pydantic import BaseModel
from typing import Optional

class roles(BaseModel):
    id: int = None
    nombre: str
    estado: Optional[bool] = None