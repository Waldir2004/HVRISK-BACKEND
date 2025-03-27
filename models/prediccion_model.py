from pydantic import BaseModel
from typing import Optional

class prediccion(BaseModel):
    id: Optional[int] = None
    usuario_id: int
    edad: int
    genero: int
    altura_cm: float
    peso_kg: float
    presion_sistolica: int
    presion_diastolica: int
    colesterol: int
    glucosa: int
    fuma: bool
    alcohol: bool
    dieta: bool
    actividad_fisica: bool
    antecedentes_familiares: bool
    diabetes: bool
    prediccion_riesgo: Optional[str] = None
