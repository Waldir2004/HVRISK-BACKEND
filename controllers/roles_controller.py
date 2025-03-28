import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.roles_models import Roles
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import datetime

class RolesController:
    def crear_rol(self, rol: Roles) -> dict:
        """Crea un nuevo rol en el sistema"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Validación del nombre
            if not rol.nombre or len(rol.nombre) > 50:
                raise HTTPException(
                    status_code=400,
                    detail="El nombre es requerido (max 50 caracteres)"
                )
            
            cursor.execute(
                "INSERT INTO roles (nombre, estado) VALUES (%s, %s)", 
                (rol.nombre, rol.estado)
            )
            rol_id = cursor.lastrowid
            conn.commit()
            
            return {
                "resultado": "Rol creado exitosamente",
                "id": rol_id,
                "nombre": rol.nombre
            }
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear rol: {err}"
            )
        finally:
            conn.close()

    def listar_roles(self) -> dict:
        """Obtiene todos los roles activos"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT id, nombre, estado 
                FROM roles 
                WHERE deleted_at IS NULL
                ORDER BY nombre ASC
            """)
            
            result = cursor.fetchall()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontraron roles"
                )
                
            return {"roles": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al listar roles: {err}"
            )
        finally:
            conn.close()

    def obtener_rol(self, rol_id: int) -> dict:
        """Obtiene un rol específico por su ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT id, nombre, estado 
                FROM roles 
                WHERE id = %s AND deleted_at IS NULL
            """, (rol_id,))
            
            result = cursor.fetchone()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Rol no encontrado"
                )
                
            return {"rol": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener rol: {err}"
            )
        finally:
            conn.close()

    def actualizar_rol(self, rol_id: int, rol: Roles) -> dict:
        """Actualiza un rol existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Validación del nombre
            if rol.nombre and len(rol.nombre) > 50:
                raise HTTPException(
                    status_code=400,
                    detail="El nombre no puede exceder 50 caracteres"
                )
            
            query = """
                UPDATE roles SET
                    nombre = %s,
                    estado = %s,
                    updated_at = NOW()
                WHERE id = %s
            """
            cursor.execute(query, (rol.nombre, rol.estado, rol_id))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Rol no encontrado"
                )
                
            return {"resultado": "Rol actualizado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al actualizar rol: {err}"
            )
        finally:
            conn.close()

    def eliminar_rol(self, rol_id: int) -> dict:
        """Elimina lógicamente un rol"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar si el rol tiene usuarios asociados
            cursor.execute("SELECT 1 FROM usuarios WHERE rol_id = %s LIMIT 1", (rol_id,))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=400,
                    detail="No se puede eliminar el rol porque tiene usuarios asociados"
                )
            
            cursor.execute(
                "UPDATE roles SET deleted_at = NOW() WHERE id = %s",
                (rol_id,)
            )
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Rol no encontrado"
                )
                
            return {"resultado": "Rol eliminado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al eliminar rol: {err}"
            )
        finally:
            conn.close()