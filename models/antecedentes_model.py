from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Antecedentes(BaseModel):
    id: int = None
    paciente_id: int
    diabetes: Optional[bool] = None
    hipertension: Optional[bool] = None
    enfermedad_renal: Optional[bool] = None
    apnea_sueno: Optional[bool] = None
    tabaquismo: Optional[bool] = None
    familia_cardiopatia: Optional[bool] = None
