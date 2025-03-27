import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.permisos_models import permisos
from fastapi.encoders import jsonable_encoder
from typing import List
from datetime import datetime

class PermisosController:
    def create_permiso(self, permiso: permisos):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO permisos (modulo_id, rol_id, estado) VALUES (%s, %s, %s)",
                (permiso.modulo_id, permiso.rol_id, permiso.estado)
            )
            conn.commit()
            return {"resultado": "Permiso creado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_permisos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, modulo_id, rol_id, estado FROM permisos WHERE deleted_at IS NULL")
            result = cursor.fetchall()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Permisos no encontrados")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_permiso(self, permiso_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, modulo_id, rol_id, estado FROM permisos WHERE id = %s AND deleted_at IS NULL", (permiso_id,))
            result = cursor.fetchone()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Permiso no encontrado")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def edit_permiso(self, permiso_id: int, permiso: permisos):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE permisos SET modulo_id = %s, rol_id = %s, estado = %s WHERE id = %s",
                (permiso.modulo_id, permiso.rol_id, permiso.estado, permiso_id)
            )
            conn.commit()
            return {"resultado": "Permiso actualizado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_permiso(self, permiso_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            deleted_at = datetime.now()
            cursor.execute("UPDATE permisos SET deleted_at = %s WHERE id = %s", (deleted_at, permiso_id))
            conn.commit()
            return {"resultado": "Permiso eliminado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_permisos_por_rol(self, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT modulo_id FROM permisos WHERE rol_id = %s AND estado = '1' AND deleted_at IS NULL", (rol_id,))
            results = cursor.fetchall()
            if results:
                modulo_ids = [result['modulo_id'] for result in results]
                return {"modulos": modulo_ids}
            else:
                raise HTTPException(status_code=404, detail="No se encontraron permisos para este rol")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def edit_permisos_por_rol(self, rol_id: int, permisos: List[permisos]):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Eliminar permisos existentes para el rol
            cursor.execute("DELETE FROM permisos WHERE rol_id = %s", (rol_id,))

            # Insertar nuevos permisos
            for permiso in permisos:
                cursor.execute(
                    "INSERT INTO permisos (modulo_id, rol_id, estado) VALUES (%s, %s, %s)",
                    (permiso.modulo_id, rol_id, permiso.estado)
                )

            conn.commit()
            return {"resultado": "Permisos actualizados"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()