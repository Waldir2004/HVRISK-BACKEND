from pydantic import BaseModel
from typing import Optional

class ParametrosValor(BaseModel):
    id: int = None
    refencia: str
    nombre: str
    descripcion: str
    parametro_id:int
    estado: Optional[bool] = None