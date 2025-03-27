import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.enfermedades_models import enfermedades
from fastapi.encoders import jsonable_encoder
from typing import List
from datetime import datetime

class EnfermedadesController:
    def create_enfermedad(self, enfermedad: enfermedades):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO enfermedades (nombre, categoria_id, estado) 
                VALUES (%s, %s, %s)""",
                (enfermedad.nombre, enfermedad.categoria_id, enfermedad.estado)
            )
            conn.commit()
            return {"resultado": "Enfermedad creada"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_enfermedades(self) -> List[dict]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM enfermedades WHERE deleted_at IS NULL")
            result = cursor.fetchall()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Enfermedades no encontradas")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_enfermedad(self, enfermedad_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM enfermedades WHERE id = %s AND deleted_at IS NULL", (enfermedad_id,))
            result = cursor.fetchone()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Enfermedad no encontrada")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def edit_enfermedad(self, enfermedad_id: int, enfermedad: enfermedades):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE enfermedades SET nombre = %s, categoria_id = %s, estado = %s 
                WHERE id = %s""",
                (enfermedad.nombre, enfermedad.categoria_id, enfermedad.estado, enfermedad_id)
            )
            conn.commit()
            return {"resultado": "Enfermedad actualizada"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_enfermedad(self, enfermedad_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            deleted_at = datetime.now()
            cursor.execute("UPDATE enfermedades SET deleted_at = %s WHERE id = %s", (deleted_at, enfermedad_id))
            conn.commit()
            return {"resultado": "Enfermedad eliminada"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
