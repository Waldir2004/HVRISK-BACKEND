from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DatosClinicos(BaseModel):
    id: int = None
    paciente_id: int
    peso_kg: Optional[float] = None
    altura_cm: Optional[float] = None
    circ_cintura_cm: Optional[float] = None
    presion_sistolica: Optional[int] = None
    presion_diastolica: Optional[int] = None
    frecuencia_cardiaca: Optional[int] = None