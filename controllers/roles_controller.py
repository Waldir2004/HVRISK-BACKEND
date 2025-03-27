import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.roles_models import roles
from fastapi.encoders import jsonable_encoder
from typing import List
from datetime import datetime

class RolesController:
    def create_role(self, role: roles):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO roles (nombre, estado) VALUES (%s, %s)", 
                (role.nombre, role.estado)
            )
            role_id = cursor.lastrowid  # Obtener el ID del rol recién creado
            conn.commit()
            conn.close()
            return {"resultado": "Rol creado", "id": role_id}  # Incluir el ID en la respuesta
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()


    def get_roles(self) -> List[dict]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre, estado FROM roles WHERE deleted_at IS NULL")
            result = cursor.fetchall()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Roles no encontrados")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_role(self, role_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre, estado FROM roles WHERE id = %s AND deleted_at IS NULL", (role_id,))
            result = cursor.fetchone()
            if result:
                json_data = jsonable_encoder(result)
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="Rol no encontrado")
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def edit_role(self, role_id: int, role: roles):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE roles SET nombre = %s, estado = %s WHERE id = %s", 
                (role.nombre, role.estado, role_id)
            )
            conn.commit()
            conn.close()
            return {"resultado": "Rol actualizado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_role(self, role_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            deleted_at = datetime.now()
            cursor.execute("UPDATE roles SET deleted_at = %s WHERE id = %s", (deleted_at, role_id))
            conn.commit()
            return {"resultado": "Rol eliminado"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
