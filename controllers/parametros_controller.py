import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.parametros_models import Parametros
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import datetime

class ParametrosController:
    def crear_parametro(self, parametro: Parametros) -> dict:
        """Crea un nuevo parámetro en el sistema"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Validación adicional (ejemplo)
            if not parametro.referencia or len(parametro.referencia) > 20:
                raise HTTPException(
                    status_code=400,
                    detail="La referencia es requerida (max 20 caracteres)"
                )
            
            query = """
                INSERT INTO parametros (referencia, nombre, descripcion, estado)
                VALUES (%s, %s, %s, %s)
            """
            values = (
                parametro.referencia,
                parametro.nombre,
                parametro.descripcion,
                parametro.estado
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            return {
                "resultado": "Parámetro creado exitosamente",
                "id": cursor.lastrowid,
                "referencia": parametro.referencia
            }
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear parámetro: {err}"
            )
        finally:
            conn.close()

    def listar_parametros(self) -> List[dict]:
        """Obtiene todos los parámetros activos"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT id, referencia, nombre, descripcion, estado 
                FROM parametros 
                WHERE deleted_at IS NULL
                ORDER BY nombre ASC
            """)
            
            result = cursor.fetchall()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontraron parámetros"
                )
                
            return {"parametros": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener parámetros: {err}"
            )
        finally:
            conn.close()

    def obtener_parametro(self, parametro_id: int) -> dict:
        """Obtiene un parámetro específico por su ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT id, referencia, nombre, descripcion, estado 
                FROM parametros 
                WHERE id = %s AND deleted_at IS NULL
            """, (parametro_id,))
            
            result = cursor.fetchone()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Parámetro no encontrado"
                )
                
            return {"parametro": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener parámetro: {err}"
            )
        finally:
            conn.close()

    def actualizar_parametro(self, parametro_id: int, parametro: Parametros) -> dict:
        """Actualiza un parámetro existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE parametros SET
                    referencia = %s,
                    nombre = %s,
                    descripcion = %s,
                    estado = %s,
                    updated_at = NOW()
                WHERE id = %s
            """
            values = (
                parametro.referencia,
                parametro.nombre,
                parametro.descripcion,
                parametro.estado,
                parametro_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Parámetro no encontrado"
                )
                
            return {"resultado": "Parámetro actualizado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al actualizar parámetro: {err}"
            )
        finally:
            conn.close()

    def eliminar_parametro(self, parametro_id: int) -> dict:
        """Elimina lógicamente un parámetro"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE parametros SET deleted_at = NOW() WHERE id = %s",
                (parametro_id,)
            )
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Parámetro no encontrado"
                )
                
            return {"resultado": "Parámetro eliminado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al eliminar parámetro: {err}"
            )
        finally:
            conn.close()