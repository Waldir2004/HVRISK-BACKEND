import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.datos_clinicos_model import DatosClinicos
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import datetime

class DatosClinicosController:
    def create_datos_clinicos(self, datos: DatosClinicos) -> dict:
        """Crea un nuevo registro de datos clínicos"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO datos_clinicos (
                    evaluacion_id, peso_kg, altura_cm, circ_cintura_cm,
                    presion_sistolica, presion_diastolica, frecuencia_cardiaca,
                    ldl, hdl, trigliceridos, glucosa_ayunas, hba1c, creatinina
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                datos.evaluacion_id,
                datos.peso_kg,
                datos.altura_cm,
                datos.circ_cintura_cm,
                datos.presion_sistolica,
                datos.presion_diastolica,
                datos.frecuencia_cardiaca,
                datos.ldl,
                datos.hdl,
                datos.trigliceridos,
                datos.glucosa_ayunas,
                datos.hba1c,
                datos.creatinina,
            )
            
            cursor.execute(query, values)
            conn.commit()
            return {
                "resultado": "Datos clínicos creados exitosamente",
                "id": cursor.lastrowid
            }
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
        finally:
            conn.close()

    def get_datos_clinicos(self, evaluacion_id: Optional[int] = None) -> List[dict]:
        """Obtiene todos los registros o filtra por evaluacion_id"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            base_query = "SELECT * FROM datos_clinicos WHERE deleted_at IS NULL"
            if evaluacion_id:
                base_query += " AND evaluacion_id = %s"
                cursor.execute(base_query, (evaluacion_id,))
            else:
                cursor.execute(base_query)
                
            result = cursor.fetchall()
            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron registros")
                
            return {"resultado": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
        finally:
            conn.close()

    def get_datos_clinicos_by_id(self, datos_id: int) -> dict:
        """Obtiene un registro específico por ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT * FROM datos_clinicos WHERE id = %s AND deleted_at IS NULL",
                (datos_id,)
            )
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(status_code=404, detail="Registro no encontrado")
                
            return {"resultado": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
        finally:
            conn.close()

    def update_datos_clinicos(self, datos_id: int, datos: DatosClinicos) -> dict:
        """Actualiza un registro existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
               UPDATE datos_clinicos SET
                    evaluacion_id = %s,
                    peso_kg = %s,
                    altura_cm = %s,
                    circ_cintura_cm = %s,
                    presion_sistolica = %s,
                    presion_diastolica = %s,
                    frecuencia_cardiaca = %s,
                    ldl = %s,
                    hdl = %s,
                    trigliceridos = %s,
                    glucosa_ayunas = %s,
                    hba1c = %s,
                    creatinina = %s,
                WHERE id = %s
            """
            values = (
                datos.evaluacion_id,
                datos.peso_kg,
                datos.altura_cm,
                datos.circ_cintura_cm,
                datos.presion_sistolica,
                datos.presion_diastolica,
                datos.frecuencia_cardiaca,
                datos.ldl,
                datos.hdl,
                datos.trigliceridos,
                datos.glucosa_ayunas,
                datos.hba1c,
                datos.creatinina,
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Registro no encontrado")
                
            return {"resultado": "Datos clínicos actualizados exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
        finally:
            conn.close()

    def delete_datos_clinicos(self, datos_id: int) -> dict:
        """Eliminación lógica de un registro"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE datos_clinicos SET deleted_at = NOW() WHERE id = %s",
                (datos_id,)
            )
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Registro no encontrado")
                
            return {"resultado": "Datos clínicos eliminados exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
        finally:
            conn.close()