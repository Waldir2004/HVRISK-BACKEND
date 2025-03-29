from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Evaluaciones(BaseModel):
    id: int = None
    paciente_id: int
    fecha_evaluacion: Optional[datetime] = None
    riesgo_hvi_id: Optional[int] = None
    riesgo_hvd_id: Optional[int] = None
    puntuacion_hvi: Optional[int] = None
    puntuacion_hvd: Optional[int] = None
    framingham_risk: Optional[int] = None
    notas: Optional[str] = None