import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.antecedentes_model import Antecedentes
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import datetime

class AntecedentesController:
    def create_antecedente(self, antecedente: Antecedentes) -> dict:
        """Crea un nuevo registro de antecedentes médicos"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO antecedentes_medicos (
                    evaluacion_id, diabetes, hipertension, enfermedad_renal,
                    apnea_sueno, dislipidemia, epoc, familia_cardiopatia,
                    familia_diabetes, tabaquismo_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                antecedente.evaluacion_id,
                antecedente.diabetes,
                antecedente.hipertension,
                antecedente.enfermedad_renal,
                antecedente.apnea_sueno,
                antecedente.dislipidemia,
                antecedente.epoc,
                antecedente.familia_cardiopatia,
                antecedente.familia_diabetes,
                antecedente.tabaquismo_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            return {"resultado": "Antecedente creado exitosamente", "id": cursor.lastrowid}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
        finally:
            conn.close()

    def get_antecedentes(self, evaluacion_id: Optional[int] = None) -> List[dict]:
        """Obtiene todos los antecedentes o filtra por evaluation_id"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            base_query = "SELECT * FROM antecedentes_medicos WHERE deleted_at IS NULL"
            if evaluacion_id:
                base_query += " AND evaluacion_id = %s"
                cursor.execute(base_query, (evaluacion_id,))
            else:
                cursor.execute(base_query)
                
            result = cursor.fetchall()
            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron antecedentes")
                
            return {"resultado": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
        finally:
            conn.close()

    def get_antecedente(self, antecedente_id: int) -> dict:
        """Obtiene un antecedente específico por su ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT * FROM antecedentes_medicos WHERE id = %s AND deleted_at IS NULL",
                (antecedente_id,)
            )
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(status_code=404, detail="Antecedente no encontrado")
                
            return {"resultado": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
        finally:
            conn.close()

    def update_antecedente(self, antecedente_id: int, antecedente: Antecedentes) -> dict:
        """Actualiza un antecedente médico existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE antecedentes_medicos SET
                    evaluacion_id = %s,
                    diabetes = %s,
                    hipertension = %s,
                    enfermedad_renal = %s,
                    apnea_sueno = %s,
                    dislipidemia = %s,
                    epoc = %s,
                    familia_cardiopatia = %s,
                    familia_diabetes = %s,
                    tabaquismo_id = %s,
                    updated_at = NOW()
                WHERE id = %s
            """
            values = (
                antecedente.evaluacion_id,
                antecedente.diabetes,
                antecedente.hipertension,
                antecedente.enfermedad_renal,
                antecedente.apnea_sueno,
                antecedente.dislipidemia,
                antecedente.epoc,
                antecedente.familia_cardiopatia,
                antecedente.familia_diabetes,
                antecedente.tabaquismo_id,
                antecedente_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Antecedente no encontrado")
                
            return {"resultado": "Antecedente actualizado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
        finally:
            conn.close()