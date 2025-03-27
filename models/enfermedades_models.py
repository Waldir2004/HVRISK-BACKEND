from pydantic import BaseModel
from typing import Optional

class enfermedades(BaseModel):
    id: int = None
    nombre: str
    categoria_id: int
    estado: Optional[bool] = None