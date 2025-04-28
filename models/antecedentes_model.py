from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Antecedentes(BaseModel):
    id: int = None
    evaluacion_id: int
    diabetes: Optional[bool] = False
    hipertension: Optional[bool] = False
    enfermedad_renal: Optional[bool] = False
    apnea_sueno: Optional[bool] = False
    dislipidemia: Optional[bool] = False
    epoc: Optional[bool] = False
    familia_cardiopatia: Optional[bool] = False
    familia_diabetes: Optional[bool] = False
    tabaquismo_id: Optional[int] = None