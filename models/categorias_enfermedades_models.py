from pydantic import BaseModel
from typing import Optional

class Categorias_enfermedades(BaseModel):
    id: int = None
    nombre: str
    estado: Optional[bool] = None