from pydantic import BaseModel

class Auth(BaseModel):
    id: int=None
    correo_electronico: str
    contraseña: str