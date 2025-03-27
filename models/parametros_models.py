from pydantic import BaseModel
from typing import Optional

class parametros(BaseModel):
    id: int = None
    refencia: str
    nombre: str
    descripcion: str
    estado: Optional[bool] = None