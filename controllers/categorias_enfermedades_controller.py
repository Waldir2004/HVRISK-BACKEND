import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.categorias_enfermedades_models import Categorias_enfermedades
from fastapi.encoders import jsonable_encoder
from typing import List
from datetime import datetime

class CategoriasEnfermedadesController:
    def create_categoria(self, categoria: Categorias_enfermedades):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO categorias_enfermedades (nombre, estado) 
                VALUES (%s, %s)""",
                (categoria.nombre, categoria.estado)
            )
            conn.commit()
            return {"resultado": "Categoría de enfermedad creada"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_categorias(self) -> List[dict]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM categorias_enfermedades WHERE deleted_at IS NULL")
            result = cursor.fetchall()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Categorías no encontradas")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_categoria(self, categoria_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM categorias_enfermedades WHERE id = %s AND deleted_at IS NULL", (categoria_id,))
            result = cursor.fetchone()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Categoría no encontrada")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def edit_categoria(self, categoria_id: int, categoria: Categorias_enfermedades):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE categorias_enfermedades SET nombre = %s, estado = %s 
                WHERE id = %s""",
                (categoria.nombre, categoria.estado, categoria_id)
            )
            conn.commit()
            return {"resultado": "Categoría de enfermedad actualizada"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_categoria(self, categoria_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            deleted_at = datetime.now()
            cursor.execute("UPDATE categorias_enfermedades SET deleted_at = %s WHERE id = %s", (deleted_at, categoria_id))
            conn.commit()
            return {"resultado": "Categoría de enfermedad eliminada"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
