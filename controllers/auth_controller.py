import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.auth_model import Auth
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
import jwt

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthController:
        
    def login(self, auth: Auth):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)  # Resultados como diccionarios
            
            cursor.execute("""
                SELECT 
                    u.id, 
                    u.usuario,
                    u.correo_electronico, 
                    u.contraseña, 
                    u.rol_id, 
                    r.nombre AS nombre_rol, 
                    u.nombre, 
                    u.apellido, 
                    u.telefono, 
                    u.estado, 
                    u.foto_usuario,
                    u.foto_google
                FROM usuarios u
                JOIN roles r ON u.rol_id = r.id
                WHERE u.correo_electronico = %s OR u.usuario = %s
            """, (auth.correo_electronico, auth.correo_electronico))
            
            user_data = cursor.fetchone()
            conn.close()
            
            if not user_data:
                return None

            # Acceso por nombre de campo en lugar de índice numérico
            if not user_data['estado']:  # Verifica si el usuario está activo
                raise HTTPException(status_code=403, detail="Usuario no está activo")
            
            # Verificar contraseña con passlib
            if not pwd_context.verify(auth.contraseña, user_data['contraseña']):
                return None
                
            # Preparar datos para el token (sin la contraseña)
            user_token = { 
                "id": user_data['id'],
                "usuario": user_data['usuario'],
                "correo_electronico": user_data['correo_electronico'],
                "rol_id": user_data['rol_id'],
                "nombre_rol": user_data['nombre_rol'],
                "nombre": user_data['nombre'],
                "apellido": user_data['apellido'],
                "telefono": user_data['telefono'],
                "estado": user_data['estado'],
                "foto_usuario": user_data['foto_usuario'],
                "foto_google": user_data['foto_google']
            }
            return user_token
            
        except mysql.connector.Error as err:
            if 'conn' in locals():
                conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error de base de datos: {err}"
            )
       
    def create_access_token(self, data: dict, google_data: dict = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        
        # Añadir datos de Google si están disponibles
        if google_data:
            to_encode.update({
                "photo_url": google_data.get("photoURL"),
                "google_uid": google_data.get("uid"),
                "display_name": google_data.get("displayName")
            })
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
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

    def verify_google_user(self, email: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.usuario, u.correo_electronico, u.rol_id, r.nombre AS nombre_rol, 
                    u.nombre, u.apellido, u.telefono, u.estado, u.foto_usuario, u.foto_google
                FROM usuarios u
                JOIN roles r ON u.rol_id = r.id
                WHERE u.correo_electronico = %s
            """, (email,))
            user_data = cursor.fetchone()
            conn.close()
            
            if not user_data:
                return None
                
            if not user_data[7]:  # Verifica si el usuario está activo
                raise HTTPException(status_code=403, detail="Usuario no está activo")
                
            return {
                "id": user_data[0],
                "usuario": user_data[1],
                "correo_electronico": user_data[2],
                "rol_id": user_data[3],
                "nombre_rol": user_data[4],
                "nombre": user_data[5],
                "apellido": user_data[6],
                "telefono": user_data[7],
                "estado": user_data[8],
                "foto_usuario": user_data[9],
                "foto_google": user_data[10]

            }
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error de base de datos")
