import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.resultado_riesgo_model import ResultadosRiesgo
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import datetime

class ResultadoRiesgoController:
    def create_resultado(self, resultado: ResultadosRiesgo) -> dict:
        """Registra un nuevo resultado de riesgo cardiovascular"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO resultados_riesgo (
                    paciente_id, puntuacion_riesgo, nivel_riesgo_id
                ) VALUES (%s, %s, %s)
            """
            values = (
                resultado.paciente_id,
                resultado.puntuacion_riesgo,
                resultado.nivel_riesgo_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            return {
                "resultado": "Evaluación de riesgo registrada",
                "id": cursor.lastrowid,
                "puntuacion": resultado.puntuacion_riesgo,
                "nivel_riesgo": resultado.nivel_riesgo_id
            }
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al registrar evaluación: {err}"
            )
        finally:
            conn.close()

    def get_resultados(self, paciente_id: Optional[int] = None) -> List[dict]:
        """Obtiene evaluaciones de riesgo con filtro opcional por paciente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT r.*, n.nombre as nivel_riesgo 
                FROM resultados_riesgo r
                LEFT JOIN niveles_riesgo n ON r.nivel_riesgo_id = n.id
                WHERE r.deleted_at IS NULL
            """
            
            if paciente_id:
                query += " AND r.paciente_id = %s"
                cursor.execute(query, (paciente_id,))
            else:
                cursor.execute(query)
                
            result = cursor.fetchall()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontraron evaluaciones"
                )
                
            return {"evaluaciones": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener evaluaciones: {err}"
            )
        finally:
            conn.close()

    def get_resultado_by_id(self, resultado_id: int) -> dict:
        """Obtiene una evaluación específica por ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT r.*, n.nombre as nivel_riesgo 
                FROM resultados_riesgo r
                LEFT JOIN niveles_riesgo n ON r.nivel_riesgo_id = n.id
                WHERE r.id = %s AND r.deleted_at IS NULL
            """
            cursor.execute(query, (resultado_id,))
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Evaluación no encontrada"
                )
                
            return {"evaluacion": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener evaluación: {err}"
            )
        finally:
            conn.close()

    def update_resultado(self, resultado_id: int, resultado: ResultadosRiesgo) -> dict:
        """Actualiza una evaluación existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE resultados_riesgo SET
                    paciente_id = %s,
                    puntuacion_riesgo = %s,
                    nivel_riesgo_id = %s,
                    updated_at = NOW()
                WHERE id = %s
            """
            values = (
                resultado.paciente_id,
                resultado.puntuacion_riesgo,
                resultado.nivel_riesgo_id,
                resultado_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Evaluación no encontrada"
                )
                
            return {"resultado": "Evaluación actualizada exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al actualizar: {err}"
            )
        finally:
            conn.close()

    def delete_resultado(self, resultado_id: int) -> dict:
        """Elimina lógicamente una evaluación"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE resultados_riesgo SET deleted_at = NOW() WHERE id = %s",
                (resultado_id,)
            )
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Evaluación no encontrada"
                )
                
            return {"resultado": "Evaluación eliminada exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al eliminar: {err}"
            )
        finally:
            conn.close()