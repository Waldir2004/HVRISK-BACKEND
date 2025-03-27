from pydantic import BaseModel
from typing import Optional

class permisos(BaseModel):
    id: int = None
    modulo_id: int
    rol_id: int
    estado: Optional[bool] = None