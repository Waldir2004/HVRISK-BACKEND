import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.modulos_models import Modulos
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import datetime

class ModulosController:
    def crear_modulo(self, modulo: Modulos) -> dict:
        """Crea un nuevo módulo en el sistema"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO modulos (nombre, descripcion, estado)
                VALUES (%s, %s, %s)
            """
            values = (
                modulo.nombre,
                modulo.descripcion,
                modulo.estado
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            return {
                "resultado": "Módulo creado exitosamente",
                "id": cursor.lastrowid
            }
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear módulo: {err}"
            )
        finally:
            conn.close()

    def listar_modulos(self) -> List[dict]:
        """Obtiene todos los módulos activos"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT id, nombre, descripcion, estado 
                FROM modulos 
                WHERE deleted_at IS NULL
            """)
            
            result = cursor.fetchall()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontraron módulos"
                )
                
            return {"modulos": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener módulos: {err}"
            )
        finally:
            conn.close()

    def obtener_modulo(self, modulo_id: int) -> dict:
        """Obtiene un módulo específico por su ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT id, nombre, descripcion, estado 
                FROM modulos 
                WHERE id = %s AND deleted_at IS NULL
            """, (modulo_id,))
            
            result = cursor.fetchone()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Módulo no encontrado"
                )
                
            return {"modulo": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener módulo: {err}"
            )
        finally:
            conn.close()

    def actualizar_modulo(self, modulo_id: int, modulo: Modulos) -> dict:
        """Actualiza un módulo existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE modulos SET
                    nombre = %s,
                    descripcion = %s,
                    estado = %s,
                    updated_at = NOW()
                WHERE id = %s
            """
            values = (
                modulo.nombre,
                modulo.descripcion,
                modulo.estado,
                modulo_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Módulo no encontrado"
                )
                
            return {"resultado": "Módulo actualizado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al actualizar módulo: {err}"
            )
        finally:
            conn.close()

    def eliminar_modulo(self, modulo_id: int) -> dict:
        """Elimina lógicamente un módulo"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE modulos SET deleted_at = NOW() WHERE id = %s",
                (modulo_id,)
            )
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Módulo no encontrado"
                )
                
            return {"resultado": "Módulo eliminado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al eliminar módulo: {err}"
            )
        finally:
            conn.close()