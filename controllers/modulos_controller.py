import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.modulos_models import modulos
from fastapi.encoders import jsonable_encoder
from typing import List
from datetime import datetime

class ModulosController:
    def create_modulo(self, modulo: modulos):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO modulos (nombre, descripcion, estado) VALUES (%s, %s, %s)",
                (modulo.nombre, modulo.descripcion, modulo.estado)
            )
            conn.commit()
            return {"resultado": "Módulo creado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_modulos(self) -> List[dict]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre, descripcion, estado FROM modulos WHERE deleted_at IS NULL")
            result = cursor.fetchall()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Módulos no encontrados")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_modulo(self, modulo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre, descripcion, estado FROM modulos WHERE id = %s AND deleted_at IS NULL", (modulo_id,))
            result = cursor.fetchone()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Módulo no encontrado")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def edit_modulo(self, modulo_id: int, modulo: modulos):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE modulos SET nombre = %s, descripcion = %s, estado = %s WHERE id = %s",
                (modulo.nombre, modulo.descripcion, modulo.estado, modulo_id)
            )
            conn.commit()
            return {"resultado": "Módulo actualizado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_modulo(self, modulo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            deleted_at = datetime.now()
            cursor.execute("UPDATE modulos SET deleted_at = %s WHERE id = %s", (deleted_at, modulo_id))
            conn.commit()
            return {"resultado": "Módulo eliminado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
