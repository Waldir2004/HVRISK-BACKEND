import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.user_models import Users
from fastapi.encoders import jsonable_encoder
from datetime import datetime

class UsersController:
    def create_user(self, user: Users):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuarios (rol_id, correo_electronico, contraseña, nombre, apellido, fecha_nacimiento, 
                    tipo_identificacion, numero_identificacion, genero, telefono, direccion, foto_usuario, estado) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user.rol_id, user.correo_electronico, user.contraseña, user.nombre, user.apellido, user.fecha_nacimiento, 
                  user.tipo_identificacion, user.numero_identificacion, user.genero, user.telefono, 
                  user.direccion, user.foto_usuario, user.estado))
            conn.commit()
            return {"resultado": "Usuario creado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT u.id, u.rol_id, u.correo_electronico, u.contraseña, u.nombre, u.apellido, 
                    u.fecha_nacimiento, u.tipo_identificacion, u.numero_identificacion, u.genero, 
                    u.telefono, u.direccion, u.foto_usuario, u.estado 
                FROM usuarios u 
                WHERE u.id = %s AND u.deleted_at IS NULL
            """, (user_id,))
            result = cursor.fetchone()
            if result:
                return {"resultado": jsonable_encoder(result)}
            else:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
            SELECT u.id, r.nombre AS rol_nombre, u.correo_electronico, u.contraseña, u.nombre, u.apellido, 
                u.fecha_nacimiento, p1.nombre AS tipo_identificacion, u.numero_identificacion, p2.nombre AS genero, 
                u.telefono, u.direccion, u.foto_usuario, u.estado 
            FROM usuarios u 
            LEFT JOIN roles r ON u.rol_id = r.id
            LEFT JOIN parametros_valor p1 ON u.tipo_identificacion = p1.id
            LEFT JOIN parametros_valor p2 ON u.genero = p2.id
            WHERE u.deleted_at IS NULL
        """)
            result = cursor.fetchall()
            if result:
                return {"resultado": jsonable_encoder(result)}
            else:
                raise HTTPException(status_code=404, detail="Usuarios no encontrados")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def edit_user(self, user_id: int, user: Users):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE usuarios SET rol_id = %s, correo_electronico = %s, contraseña = %s, nombre = %s, 
                    apellido = %s, fecha_nacimiento = %s, tipo_identificacion = %s, numero_identificacion = %s, 
                    genero = %s, telefono = %s, direccion = %s, foto_usuario = %s, estado = %s 
                WHERE id = %s
            """, (user.rol_id, user.correo_electronico, user.contraseña, user.nombre, user.apellido, 
                  user.fecha_nacimiento, user.tipo_identificacion, user.numero_identificacion, 
                  user.genero, user.telefono, user.direccion, user.foto_usuario, user.estado, user_id))
            conn.commit()
            return {"resultado": "Usuario editado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_user(self, user_id: int):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            deleted_at = datetime.now()
            cursor.execute("UPDATE usuarios SET deleted_at = %s WHERE id = %s", (deleted_at, user_id))
            conn.commit()
            return {"resultado": "Usuario eliminado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()