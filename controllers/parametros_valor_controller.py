import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.parametros_valor_models import parametros_valor
from fastapi.encoders import jsonable_encoder
from typing import List
from datetime import datetime

class ParametrosValorController:
    def create_parametro_valor(self, parametro_valor: parametros_valor):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO parametros_valor (refencia, nombre, descripcion, parametro_id, estado) VALUES (%s, %s, %s, %s, %s)",
                (parametro_valor.refencia, parametro_valor.nombre, parametro_valor.descripcion, parametro_valor.parametro_id, parametro_valor.estado)
            )
            conn.commit()
            return {"resultado": "Parámetro valor creado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_parametros_valores(self) -> List[dict]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, refencia, nombre, descripcion, parametro_id, estado FROM parametros_valor WHERE deleted_at IS NULL")
            result = cursor.fetchall()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Parámetros valores no encontrados")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_parametro_valor(self, parametro_valor_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, refencia, nombre, descripcion, parametro_id, estado FROM parametros_valor WHERE id = %s AND deleted_at IS NULL", (parametro_valor_id,))
            result = cursor.fetchone()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Parámetro valor no encontrado")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def edit_parametro_valor(self, parametro_valor_id: int, parametro_valor: parametros_valor):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE parametros_valor SET refencia = %s, nombre = %s, descripcion = %s, parametro_id = %s, estado = %s WHERE id = %s",
                (parametro_valor.refencia, parametro_valor.nombre, parametro_valor.descripcion, parametro_valor.parametro_id, parametro_valor.estado, parametro_valor_id)
            )
            conn.commit()
            return {"resultado": "Parámetro valor actualizado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_parametro_valor(self, parametro_valor_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            deleted_at = datetime.now()
            cursor.execute("UPDATE parametros_valor SET deleted_at = %s WHERE id = %s", (deleted_at, parametro_valor_id))
            conn.commit()
            return {"resultado": "Parámetro valor eliminado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_parametros_valor_por_parametro_id(self, parametro_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, referencia, nombre, descripcion, parametro_id, estado FROM parametros_valor WHERE parametro_id = %s AND deleted_at IS NULL", (parametro_id,))
            result = cursor.fetchall()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Parámetros valores no encontrados para el parametro_id proporcionado")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
