import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.auth_model import Auth
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
import jwt


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

class AuthController:
        
    def login(self, auth: Auth):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.correo_electronico, u.contraseña, u.rol_id, r.nombre AS nombre_rol, u.nombre, u.apellido, u.telefono, u.estado, u.foto_usuario
                FROM usuarios u
                JOIN roles r ON u.rol_id = r.id
                WHERE u.correo_electronico = %s
            """, (auth.correo_electronico,))
            user_data = cursor.fetchone()
            conn.close()
            if not user_data:
                return None

            if not user_data[8]:  # Verifica si el usuario está activo
                raise HTTPException(status_code=403, detail="Usuario no está activo")
            #print(user_data)
            if auth.correo_electronico==user_data[1] and auth.contraseña == user_data[2]:
                #print("CORRECTO --------------------------------------------")
                user_token={ 
                    "id": user_data[0],
                    "correo_electronico": user_data[1],
                    "contraseña": user_data[2],
                    "rol_id": user_data[3],
                    "nombre_rol": user_data[4],
                    "nombre": user_data[5],
                    "apellido": user_data[6],
                    "telefono": user_data[7],
                    "estado": user_data[8],
                    "foto_usuario": user_data[9]
                    }
                return user_token
            return None
        except mysql.connector.Error as err:
            conn.rollback()
       
    def create_access_token(self,data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        print(encoded_jwt)
        return encoded_jwt

    def validate_token(self,token,  output=False):
        try:
            if(output):
                return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.exceptions.DecodeError:
            return JSONResponse(content={"message":"Token invalido"},status_code=401)
        except jwt.exceptions.ExpiredSignatureError:
            return JSONResponse(content={"message":"Token expirado"},status_code=401)
'''

    def verify_token_expiration(self,token: str):
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            exp = payload.get("exp")
            if exp:
                return datetime.utcnow() > datetime.fromtimestamp(exp)
            return False
        except jwt.PyJWTError:
            return True
    
    def verify_token(self,token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.PyJWTError:
            raise Exception("Invalid token") 
'''
############################
