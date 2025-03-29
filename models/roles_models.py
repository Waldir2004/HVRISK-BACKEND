from pydantic import BaseModel
from typing import Optional

class Roles(BaseModel):
    id: int = None
    nombre: str
    estado: Optional[bool] = None