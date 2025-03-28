from pydantic import BaseModel

class Auth(BaseModel):
    correo_electronico: str
    contraseña: str