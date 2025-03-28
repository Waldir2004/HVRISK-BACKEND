import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.parametros_valor_models import ParametrosValor
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import datetime

class ParametrosValorController:
    def crear_parametro_valor(self, parametro_valor: ParametrosValor) -> dict:
        """Crea un nuevo valor de parámetro"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Validación de referencia
            if not parametro_valor.referencia or len(parametro_valor.referencia) > 20:
                raise HTTPException(
                    status_code=400,
                    detail="La referencia es requerida (max 20 caracteres)"
                )
            
            # Verificar existencia del parámetro padre
            cursor.execute("SELECT 1 FROM parametros WHERE id = %s", (parametro_valor.parametro_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="Parámetro padre no existe")

            query = """
                INSERT INTO parametros_valor (
                    referencia, nombre, descripcion, 
                    parametro_id, estado
                ) VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                parametro_valor.referencia,
                parametro_valor.nombre,
                parametro_valor.descripcion,
                parametro_valor.parametro_id,
                parametro_valor.estado
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            return {
                "resultado": "Valor de parámetro creado exitosamente",
                "id": cursor.lastrowid
            }
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear valor de parámetro: {err}"
            )
        finally:
            conn.close()

    def listar_parametros_valores(self) -> List[dict]:
        """Obtiene todos los valores de parámetros activos"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT pv.id, pv.referencia, pv.nombre, pv.descripcion,
                       pv.parametro_id, p.nombre as parametro_nombre,
                       pv.estado
                FROM parametros_valor pv
                JOIN parametros p ON pv.parametro_id = p.id
                WHERE pv.deleted_at IS NULL
                ORDER BY p.nombre, pv.nombre
            """)
            
            result = cursor.fetchall()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontraron valores de parámetros"
                )
                
            return {"parametros_valores": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al listar valores: {err}"
            )
        finally:
            conn.close()

    def obtener_parametro_valor(self, parametro_valor_id: int) -> dict:
        """Obtiene un valor de parámetro específico por ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT pv.id, pv.referencia, pv.nombre, pv.descripcion,
                       pv.parametro_id, p.nombre as parametro_nombre,
                       pv.estado
                FROM parametros_valor pv
                JOIN parametros p ON pv.parametro_id = p.id
                WHERE pv.id = %s AND pv.deleted_at IS NULL
            """, (parametro_valor_id,))
            
            result = cursor.fetchone()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Valor de parámetro no encontrado"
                )
                
            return {"parametro_valor": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener valor: {err}"
            )
        finally:
            conn.close()

    def actualizar_parametro_valor(self, parametro_valor_id: int, parametro_valor: ParametrosValor) -> dict:
        """Actualiza un valor de parámetro existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE parametros_valor SET
                    referencia = %s,
                    nombre = %s,
                    descripcion = %s,
                    parametro_id = %s,
                    estado = %s,
                    updated_at = NOW()
                WHERE id = %s
            """
            values = (
                parametro_valor.referencia,
                parametro_valor.nombre,
                parametro_valor.descripcion,
                parametro_valor.parametro_id,
                parametro_valor.estado,
                parametro_valor_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Valor de parámetro no encontrado"
                )
                
            return {"resultado": "Valor de parámetro actualizado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al actualizar: {err}"
            )
        finally:
            conn.close()

    def eliminar_parametro_valor(self, parametro_valor_id: int) -> dict:
        """Elimina lógicamente un valor de parámetro"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE parametros_valor SET deleted_at = NOW() WHERE id = %s",
                (parametro_valor_id,)
            )
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Valor de parámetro no encontrado"
                )
                
            return {"resultado": "Valor de parámetro eliminado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al eliminar: {err}"
            )
        finally:
            conn.close()

    def listar_valores_por_parametro(self, parametro_id: int) -> dict:
        """Obtiene todos los valores asociados a un parámetro específico"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT pv.id, pv.referencia, pv.nombre, pv.descripcion, 
                       pv.estado
                FROM parametros_valor pv
                WHERE pv.parametro_id = %s AND pv.deleted_at IS NULL
                ORDER BY pv.nombre
            """, (parametro_id,))
            
            result = cursor.fetchall()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontraron valores para este parámetro"
                )
                
            return {"valores": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al listar valores: {err}"
            )
        finally:
            conn.close()