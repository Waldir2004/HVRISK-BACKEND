from pydantic import BaseModel
from typing import Optional
from datetime import date

class Usuario(BaseModel):
    id: int = None
    rol_id: int
    correo_electronico: str
    contraseña: str
    nombre: str
    apellido: str
    fecha_nacimiento: date
    tipo_identificacion: int
    numero_identificacion: str
    genero: int
    telefono: int
    direccion: str
    foto_usuario: Optional[str] = None
    estado: Optional[bool] = None