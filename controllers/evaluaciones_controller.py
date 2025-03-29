import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.evaluaciones_model import Evaluaciones
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import datetime

class EvaluacionesController:
    def create_evaluacion(self, evaluacion: Evaluaciones) -> dict:
        """Registra una nueva evaluación de riesgo cardiovascular"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO evaluaciones (
                    paciente_id, riesgo_hvi_id, riesgo_hvd_id,
                    puntuacion_hvi, puntuacion_hvd, framingham_risk, notas
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                evaluacion.paciente_id,
                evaluacion.riesgo_hvi_id,
                evaluacion.riesgo_hvd_id,
                evaluacion.puntuacion_hvi,
                evaluacion.puntuacion_hvd,
                evaluacion.framingham_risk,
                evaluacion.notas
            )
            
            cursor.execute(query, values)
            conn.commit()
            return {
                "resultado": "Evaluación registrada exitosamente",
                "id": cursor.lastrowid
            }
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al registrar evaluación: {err}"
            )
        finally:
            conn.close()

    def get_evaluaciones(self, paciente_id: Optional[int] = None) -> List[dict]:
        """Obtiene evaluaciones con filtro opcional por paciente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT e.*, 
                       pv_hvi.valor as riesgo_hvi, 
                       pv_hvd.valor as riesgo_hvd
                FROM evaluaciones e
                LEFT JOIN parametros_valor pv_hvi ON e.riesgo_hvi_id = pv_hvi.id
                LEFT JOIN parametros_valor pv_hvd ON e.riesgo_hvd_id = pv_hvd.id
                WHERE e.deleted_at IS NULL
            """
            
            if paciente_id:
                query += " AND e.paciente_id = %s"
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

    def get_evaluacion_by_id(self, evaluacion_id: int) -> dict:
        """Obtiene una evaluación específica por ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT e.*, 
                       pv_hvi.valor as riesgo_hvi, 
                       pv_hvd.valor as riesgo_hvd
                FROM evaluaciones e
                LEFT JOIN parametros_valor pv_hvi ON e.riesgo_hvi_id = pv_hvi.id
                LEFT JOIN parametros_valor pv_hvd ON e.riesgo_hvd_id = pv_hvd.id
                WHERE e.id = %s AND e.deleted_at IS NULL
            """
            cursor.execute(query, (evaluacion_id,))
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

    def update_evaluacion(self, evaluacion_id: int, evaluacion: Evaluaciones) -> dict:
        """Actualiza una evaluación existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE evaluaciones SET
                    paciente_id = %s,
                    riesgo_hvi_id = %s,
                    riesgo_hvd_id = %s,
                    puntuacion_hvi = %s,
                    puntuacion_hvd = %s,
                    framingham_risk = %s,
                    notas = %s,
                    updated_at = NOW()
                WHERE id = %s
            """
            values = (
                evaluacion.paciente_id,
                evaluacion.riesgo_hvi_id,
                evaluacion.riesgo_hvd_id,
                evaluacion.puntuacion_hvi,
                evaluacion.puntuacion_hvd,
                evaluacion.framingham_risk,
                evaluacion.notas,
                evaluacion_id
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

    def delete_evaluacion(self, evaluacion_id: int) -> dict:
        """Elimina lógicamente una evaluación"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE evaluaciones SET deleted_at = NOW() WHERE id = %s",
                (evaluacion_id,)
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