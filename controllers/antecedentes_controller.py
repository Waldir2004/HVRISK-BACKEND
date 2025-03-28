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
                INSERT INTO antecedentes (
                    paciente_id, diabetes, hipertension, enfermedad_renal,
                    apnea_sueno, tabaquismo, familia_cardiopatia
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                antecedente.paciente_id,
                antecedente.diabetes,
                antecedente.hipertension,
                antecedente.enfermedad_renal,
                antecedente.apnea_sueno,
                antecedente.tabaquismo,
                antecedente.familia_cardiopatia
            )
            
            cursor.execute(query, values)
            conn.commit()
            return {"resultado": "Antecedente creado exitosamente", "id": cursor.lastrowid}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
        finally:
            conn.close()

    def get_antecedentes(self, paciente_id: Optional[int] = None) -> List[dict]:
        """Obtiene todos los antecedentes o filtra por paciente_id"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            base_query = "SELECT * FROM antecedentes WHERE deleted_at IS NULL"
            if paciente_id:
                base_query += " AND paciente_id = %s"
                cursor.execute(base_query, (paciente_id,))
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
                "SELECT * FROM antecedentes WHERE id = %s AND deleted_at IS NULL",
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
                UPDATE antecedentes SET
                    paciente_id = %s,
                    diabetes = %s,
                    hipertension = %s,
                    enfermedad_renal = %s,
                    apnea_sueno = %s,
                    tabaquismo = %s,
                    familia_cardiopatia = %s,
                    updated_at = NOW()
                WHERE id = %s
            """
            values = (
                antecedente.paciente_id,
                antecedente.diabetes,
                antecedente.hipertension,
                antecedente.enfermedad_renal,
                antecedente.apnea_sueno,
                antecedente.tabaquismo,
                antecedente.familia_cardiopatia,
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

    def delete_antecedente(self, antecedente_id: int) -> dict:
        """Elimina (soft delete) un antecedente médico"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE antecedentes SET deleted_at = NOW() WHERE id = %s",
                (antecedente_id,)
            )
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Antecedente no encontrado")
                
            return {"resultado": "Antecedente eliminado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
        finally:
            conn.close()