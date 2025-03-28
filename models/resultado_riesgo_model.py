from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResultadosRiesgo(BaseModel):
    id: int = None
    paciente_id: int
    puntuacion_riesgo: Optional[int] = None
    nivel_riesgo_id: int