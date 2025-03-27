import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.parametros_models import parametros
from fastapi.encoders import jsonable_encoder
from typing import List
from datetime import datetime

class ParametrosController:
    def create_parametro(self, parametro: parametros):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO parametros (refencia, nombre, descripcion, estado) VALUES (%s, %s, %s, %s)",
                (parametro.refencia, parametro.nombre, parametro.descripcion, parametro.estado)
            )
            conn.commit()
            return {"resultado": "Parámetro creado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_parametros(self) -> List[dict]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, refencia, nombre, descripcion, estado FROM parametros WHERE deleted_at IS NULL")
            result = cursor.fetchall()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Parámetros no encontrados")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_parametro(self, parametro_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, refencia, nombre, descripcion, estado FROM parametros WHERE id = %s AND deleted_at IS NULL", (parametro_id,))
            result = cursor.fetchone()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Parámetro no encontrado")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def edit_parametro(self, parametro_id: int, parametro: parametros):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE parametros SET refencia = %s, nombre = %s, descripcion = %s, estado = %s WHERE id = %s",
                (parametro.refencia, parametro.nombre, parametro.descripcion, parametro.estado, parametro_id)
            )
            conn.commit()
            return {"resultado": "Parámetro actualizado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_parametro(self, parametro_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            deleted_at = datetime.now()
            cursor.execute("UPDATE parametros SET deleted_at = %s WHERE id = %s", (deleted_at, parametro_id))
            conn.commit()
            return {"resultado": "Parámetro eliminado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
