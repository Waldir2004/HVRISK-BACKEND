from pydantic import BaseModel
from typing import Optional

class modulos(BaseModel):
    id: int = None
    nombre: str
    descripcion: str
    estado: Optional[bool] = None