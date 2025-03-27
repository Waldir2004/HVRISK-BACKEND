import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.historial_usuario_model import Historial_usuario
from fastapi.encoders import jsonable_encoder
from typing import List
from datetime import datetime

class HistorialUsuarioController:
    def create_historial(self, historial: Historial_usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO historial_usuario (usuario_id, tiene_actual, enfermedad_actual_id, 
                tiene_anterior, enfermedad_anterior_id, alergias, medicacion, 
                antecedentes_familiares, observaciones) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (historial.usuario_id, historial.tiene_actual, historial.enfermedad_actual_id, 
                 historial.tiene_anterior, historial.enfermedad_anterior_id, historial.alergias, 
                 historial.medicacion, historial.antecedentes_familiares, historial.observaciones)
            )
            conn.commit()
            return {"resultado": "Historial de usuario creado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_historiales(self) -> List[dict]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM historial_usuario WHERE deleted_at IS NULL")
            result = cursor.fetchall()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Historiales de usuario no encontrados")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_historial(self, historial_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM historial_usuario WHERE id = %s AND deleted_at IS NULL", (historial_id,))
            result = cursor.fetchone()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Historial de usuario no encontrado")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def edit_historial(self, historial_id: int, historial: Historial_usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE historial_usuario SET usuario_id = %s, tiene_actual = %s, enfermedad_actual_id = %s, 
                tiene_anterior = %s, enfermedad_anterior_id = %s, alergias = %s, medicacion = %s, 
                antecedentes_familiares = %s, observaciones = %s WHERE id = %s""",
                (historial.usuario_id, historial.tiene_actual, historial.enfermedad_actual_id, 
                 historial.tiene_anterior, historial.enfermedad_anterior_id, historial.alergias, 
                 historial.medicacion, historial.antecedentes_familiares, historial.observaciones, historial_id)
            )
            conn.commit()
            return {"resultado": "Historial de usuario actualizado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_historial(self, historial_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            deleted_at = datetime.now()
            cursor.execute("UPDATE historial_usuario SET deleted_at = %s WHERE id = %s", (deleted_at, historial_id))
            conn.commit()
            return {"resultado": "Historial de usuario eliminado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
