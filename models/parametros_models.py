from pydantic import BaseModel
from typing import Optional

class Parametros(BaseModel):
    id: int = None
    refencia: str
    nombre: str
    descripcion: str
    estado: Optional[bool] = None