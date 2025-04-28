import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.estilo_vida_model import EstiloVida
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import datetime

class EstiloVidaController:
    def create_estilo_vida(self, estilo: EstiloVida) -> dict:
        """Crea un nuevo registro de estilo de vida"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO estilo_vida (
                    evaluacion_id, actividad_fisica_id, horas_ejercicio_semana,
                    consumo_alcohol_id, consumo_cafeina_id, dieta_alta_sodio,
                    dieta_alta_grasas, horas_sueno_diario, calidad_sueno_id,
                    nivel_estres_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                estilo.evaluacion_id,
                estilo.actividad_fisica_id,
                estilo.horas_ejercicio_semana,
                estilo.consumo_alcohol_id,
                estilo.consumo_cafeina_id,
                estilo.dieta_alta_sodio,
                estilo.dieta_alta_grasas,
                estilo.horas_sueno_diario,
                estilo.calidad_sueno_id,
                estilo.nivel_estres_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            return {
                "resultado": "Registro de estilo de vida creado",
                "id": cursor.lastrowid
            }
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500, 
                detail=f"Error al crear registro: {err}"
            )
        finally:
            conn.close()

    def get_estilos_vida(self, evaluacion_id: Optional[int] = None) -> List[dict]:
        """Obtiene registros de estilo de vida, con filtro opcional por evaluación"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT ev.*, 
                       af.valor as actividad_fisica,
                       ca.valor as consumo_alcohol,
                       cc.valor as consumo_cafeina,
                       cs.valor as calidad_sueno,
                       ne.valor as nivel_estres
                FROM estilo_vida ev
                LEFT JOIN parametros_valor af ON ev.actividad_fisica_id = af.id
                LEFT JOIN parametros_valor ca ON ev.consumo_alcohol_id = ca.id
                LEFT JOIN parametros_valor cc ON ev.consumo_cafeina_id = cc.id
                LEFT JOIN parametros_valor cs ON ev.calidad_sueno_id = cs.id
                LEFT JOIN parametros_valor ne ON ev.nivel_estres_id = ne.id
                WHERE ev.deleted_at IS NULL
            """
            if evaluacion_id:
                query += " AND ev.evaluacion_id = %s"
                cursor.execute(query, (evaluacion_id,))
            else:
                cursor.execute(query)
                
            result = cursor.fetchall()
            if not result:
                raise HTTPException(
                    status_code=404, 
                    detail="No se encontraron registros"
                )
                
            return {"resultado": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500, 
                detail=f"Error al obtener registros: {err}"
            )
        finally:
            conn.close()

    def get_estilo_vida_by_id(self, estilo_id: int) -> dict:
        """Obtiene un registro específico por ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT ev.*, 
                       af.valor as actividad_fisica,
                       ca.valor as consumo_alcohol,
                       cc.valor as consumo_cafeina,
                       cs.valor as calidad_sueno,
                       ne.valor as nivel_estres
                FROM estilo_vida ev
                LEFT JOIN parametros_valor af ON ev.actividad_fisica_id = af.id
                LEFT JOIN parametros_valor ca ON ev.consumo_alcohol_id = ca.id
                LEFT JOIN parametros_valor cc ON ev.consumo_cafeina_id = cc.id
                LEFT JOIN parametros_valor cs ON ev.calidad_sueno_id = cs.id
                LEFT JOIN parametros_valor ne ON ev.nivel_estres_id = ne.id
                WHERE ev.id = %s AND ev.deleted_at IS NULL
            """
            cursor.execute(query, (estilo_id,))
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(
                    status_code=404, 
                    detail="Registro no encontrado"
                )
                
            return {"resultado": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500, 
                detail=f"Error al obtener registro: {err}"
            )
        finally:
            conn.close()

    def update_estilo_vida(self, estilo_id: int, estilo: EstiloVida) -> dict:
        """Actualiza un registro existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE estilo_vida SET
                    evaluacion_id = %s,
                    actividad_fisica_id = %s,
                    horas_ejercicio_semana = %s,
                    consumo_alcohol_id = %s,
                    consumo_cafeina_id = %s,
                    dieta_alta_sodio = %s,
                    dieta_alta_grasas = %s,
                    horas_sueno_diario = %s,
                    calidad_sueno_id = %s,
                    nivel_estres_id = %s,
                    updated_at = NOW()
                WHERE id = %s
            """
            values = (
                estilo.evaluacion_id,
                estilo.actividad_fisica_id,
                estilo.horas_ejercicio_semana,
                estilo.consumo_alcohol_id,
                estilo.consumo_cafeina_id,
                estilo.dieta_alta_sodio,
                estilo.dieta_alta_grasas,
                estilo.horas_sueno_diario,
                estilo.calidad_sueno_id,
                estilo.nivel_estres_id,
                estilo_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, 
                    detail="Registro no encontrado"
                )
                
            return {"resultado": "Registro actualizado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500, 
                detail=f"Error al actualizar: {err}"
            )
        finally:
            conn.close()

  