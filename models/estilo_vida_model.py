from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EstiloVida(BaseModel):
    id: int = None
    evaluacion_id: int
    # Actividad física
    actividad_fisica_id: Optional[int] = None
    horas_ejercicio_semana: Optional[float] = None
    # Consumo sustancias
    consumo_alcohol_id: Optional[int] = None
    consumo_cafeina_id: Optional[int] = None
    # Hábitos
    dieta_alta_sodio: Optional[bool] = False
    dieta_alta_grasas: Optional[bool] = False
    horas_sueno_diario: Optional[float] = None
    calidad_sueno_id: Optional[int] = None
    nivel_estres_id: Optional[int] = None