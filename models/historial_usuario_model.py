from pydantic import BaseModel
from typing import Optional

class Historial_usuario(BaseModel):
    id: int = None
    usuario_id: int
    tiene_actual: Optional[bool] = None
    enfermedad_actual_id: int
    tiene_anterior: Optional[bool] = None
    enfermedad_anterior_id: int
    alergias: Optional[bool] = None
    medicacion: Optional[bool] = None
    antecedentes_familiares: Optional[bool] = None
    observaciones: str