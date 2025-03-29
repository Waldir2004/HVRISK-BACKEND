from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DatosClinicos(BaseModel):
    id: int = None
    evaluacion_id: int
    # Mediciones básicas
    peso_kg: Optional[float] = None
    altura_cm: Optional[float] = None
    circ_cintura_cm: Optional[float] = None
    presion_sistolica: Optional[int] = None
    presion_diastolica: Optional[int] = None
    frecuencia_cardiaca: Optional[int] = None
    # Laboratorio
    ldl: Optional[float] = None
    hdl: Optional[float] = None
    trigliceridos: Optional[float] = None
    glucosa_ayunas: Optional[float] = None
    hba1c: Optional[float] = None
    creatinina: Optional[float] = None
    # Campos calculados (deberían ser readonly)
    imc: Optional[float] = None
    presion_arterial_media: Optional[float] = None
    superficie_corporal: Optional[float] = None