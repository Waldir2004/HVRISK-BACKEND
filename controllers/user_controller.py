import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.user_models import Usuario
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import datetime
import re  # Para validación de email
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuariosController:

    def crear_usuario(self, usuario: Usuario) -> dict:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT 1 FROM usuarios WHERE usuario = %s", (usuario.usuario,))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=400,
                    detail="El nombre de usuario ya está registrado"
                )
            
            # Verificar si el rol existe
            cursor.execute("SELECT 1 FROM roles WHERE id = %s", (usuario.rol_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="Rol no válido")
            
            # Verificar si el correo ya existe
            cursor.execute("SELECT 1 FROM usuarios WHERE correo_electronico = %s", (usuario.correo_electronico,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
            
            hashed_password = pwd_context.hash(usuario.contraseña)

            query = """
                INSERT INTO usuarios (
                    rol_id, usuario, correo_electronico, contraseña, nombre, apellido,
                    fecha_nacimiento, tipo_identificacion, numero_identificacion,
                    genero, telefono, direccion, foto_usuario, foto_google, estado
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                usuario.rol_id,
                usuario.usuario,
                usuario.correo_electronico,
                hashed_password,  # Nota: Debería estar hasheada
                usuario.nombre,
                usuario.apellido,
                usuario.fecha_nacimiento,
                usuario.tipo_identificacion,
                usuario.numero_identificacion,
                usuario.genero,
                usuario.telefono,
                usuario.direccion,
                usuario.foto_usuario,
                usuario.foto_google,
                usuario.estado
            )
            
            cursor.execute(query, values)
            usuario_id = cursor.lastrowid
            conn.commit()
            
            return {
                "resultado": "Usuario creado exitosamente",
                "id": usuario_id,
                "usuario": usuario.usuario,
                "correo": usuario.correo_electronico
            }
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear usuario: {err}"
            )
        finally:
            conn.close()




    def obtener_usuario(self, usuario_id: int) -> dict:
        """Obtiene un usuario específico por su ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT u.id, u.rol_id, r.nombre as rol_nombre, u.correo_electronico,
                       u.nombre, u.apellido, u.fecha_nacimiento, 
                       u.tipo_identificacion, ti.nombre as tipo_identificacion_nombre,
                       u.numero_identificacion, u.genero, g.nombre as genero_nombre,
                       u.telefono, u.direccion, u.foto_usuario, u.estado
                FROM usuarios u
                LEFT JOIN roles r ON u.rol_id = r.id
                LEFT JOIN parametros_valor ti ON u.tipo_identificacion = ti.id
                LEFT JOIN parametros_valor g ON u.genero = g.id
                WHERE u.id = %s AND u.deleted_at IS NULL
            """
            cursor.execute(query, (usuario_id,))
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario no encontrado"
                )
                
            # No retornar la contraseña
            result.pop('contraseña', None)
                
            return {"usuario": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener usuario: {err}"
            )
        finally:
            conn.close()

    def listar_usuarios(self) -> dict:
        """Obtiene todos los usuarios activos con información relacionada"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT u.id, r.nombre AS rol_nombre, u.correo_electronico, 
                       u.nombre, u.apellido, u.fecha_nacimiento, 
                       ti.nombre AS tipo_identificacion, u.numero_identificacion, 
                       g.nombre AS genero, u.telefono, u.direccion, 
                       u.foto_usuario, u.estado 
                FROM usuarios u 
                LEFT JOIN roles r ON u.rol_id = r.id
                LEFT JOIN parametros_valor ti ON u.tipo_identificacion = ti.id
                LEFT JOIN parametros_valor g ON u.genero = g.id
                WHERE u.deleted_at IS NULL
                ORDER BY u.created_at DESC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontraron usuarios"
                )
                
            return {"usuarios": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al listar usuarios: {err}"
            )
        finally:
            conn.close()

    def listar_usuarios_por_rol(self, rol_id: int) -> dict:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT u.id, r.nombre AS rol_nombre, u.usuario, u.correo_electronico, 
                    u.nombre, u.apellido, u.fecha_nacimiento, 
                    ti.nombre AS tipo_identificacion, u.numero_identificacion, 
                    g.nombre AS genero, u.telefono, u.direccion, 
                    u.foto_usuario, u.foto_google, u.estado 
                FROM usuarios u 
                LEFT JOIN roles r ON u.rol_id = r.id
                LEFT JOIN parametros_valor ti ON u.tipo_identificacion = ti.id
                LEFT JOIN parametros_valor g ON u.genero = g.id
                WHERE u.rol_id = %s AND u.deleted_at IS NULL AND u.estado = 1
                ORDER BY u.created_at DESC;
            """
            cursor.execute(query, (rol_id,))  # Aquí se usa el parámetro rol_id
            result = cursor.fetchall()
            
            if not result:
                return {"usuarios": []}  # Devuelve lista vacía en lugar de error
                
            return {"usuarios": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al listar usuarios por rol: {err}"
            )
        finally:
            conn.close()

    def listar_pacientes_por_doctor(self, doctor_id: int) -> dict:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT u.id, r.nombre AS rol_nombre, u.usuario, u.correo_electronico, 
                    u.nombre, u.apellido, u.fecha_nacimiento, 
                    ti.nombre AS tipo_identificacion, u.numero_identificacion, 
                    g.nombre AS genero, u.telefono, u.direccion, 
                    u.foto_usuario, u.foto_google, u.estado 
                FROM usuarios u 
                LEFT JOIN roles r ON u.rol_id = r.id
                LEFT JOIN parametros_valor ti ON u.tipo_identificacion = ti.id
                LEFT JOIN parametros_valor g ON u.genero = g.id
                JOIN doctor_paciente dp ON u.id = dp.paciente_id
                WHERE u.rol_id = 3 AND u.deleted_at IS NULL AND u.estado = 1
                AND dp.doctor_id = %s
                ORDER BY u.created_at DESC;
            """
            cursor.execute(query, (doctor_id,))
            result = cursor.fetchall()
            
            if not result:
                return {"usuarios": []}
                
            return {"usuarios": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al listar pacientes por doctor: {err}"
            )
        finally:
            conn.close()

    def actualizar_usuario(self, usuario_id: int, usuario: Usuario) -> dict:
        """Actualiza los datos de un usuario existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Validaciones básicas
            if usuario.correo_electronico:
                cursor.execute(
                    "SELECT id FROM usuarios WHERE correo_electronico = %s AND id != %s", 
                    (usuario.correo_electronico, usuario_id)
                )
                if cursor.fetchone():
                    raise HTTPException(
                        status_code=400,
                        detail="El correo electrónico ya está en uso por otro usuario"
                    )
            
            query = """
                UPDATE usuarios SET
                    rol_id = %s,
                    correo_electronico = %s,
                    nombre = %s,
                    apellido = %s,
                    fecha_nacimiento = %s,
                    tipo_identificacion = %s,
                    numero_identificacion = %s,
                    genero = %s,
                    telefono = %s,
                    direccion = %s,
                    foto_usuario = %s,
                    estado = %s,
                    updated_at = NOW()
                WHERE id = %s
            """
            values = (
                usuario.rol_id,
                usuario.correo_electronico,
                usuario.nombre,
                usuario.apellido,
                usuario.fecha_nacimiento,
                usuario.tipo_identificacion,
                usuario.numero_identificacion,
                usuario.genero,
                usuario.telefono,
                usuario.direccion,
                usuario.foto_usuario,
                usuario.estado,
                usuario_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario no encontrado"
                )
                
            return {"resultado": "Usuario actualizado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al actualizar usuario: {err}"
            )
        finally:
            conn.close()

    def eliminar_usuario(self, usuario_id: int) -> dict:
        """Elimina lógicamente un usuario"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE usuarios SET deleted_at = NOW() WHERE id = %s",
                (usuario_id,)
            )
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario no encontrado"
                )
                
            return {"resultado": "Usuario eliminado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al eliminar usuario: {err}"
            )
        finally:
            conn.close()