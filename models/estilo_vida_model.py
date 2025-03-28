from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EstiloVida(BaseModel):
    id: int = None
    paciente_id: int
    actividad_fisica_id: int
    consumo_alcohol_id: int
    dieta_alta_sodio: Optional[bool] = None