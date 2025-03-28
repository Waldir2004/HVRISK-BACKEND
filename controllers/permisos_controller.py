import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.permisos_models import Permisos
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import datetime

class PermisosController:
    def crear_permiso(self, permiso: Permisos) -> dict:
        """Asigna un nuevo permiso a un rol"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar existencia del módulo y rol
            cursor.execute("SELECT 1 FROM modulos WHERE id = %s", (permiso.modulo_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="Módulo no existe")
                
            cursor.execute("SELECT 1 FROM roles WHERE id = %s", (permiso.rol_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="Rol no existe")

            cursor.execute(
                """INSERT INTO permisos (modulo_id, rol_id, estado) 
                VALUES (%s, %s, %s)""",
                (permiso.modulo_id, permiso.rol_id, permiso.estado)
            )
            conn.commit()
            
            return {
                "resultado": "Permiso creado exitosamente",
                "id": cursor.lastrowid
            }
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear permiso: {err}"
            )
        finally:
            conn.close()

    def listar_permisos(self) -> dict:
        """Obtiene todos los permisos activos"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT p.id, p.modulo_id, m.nombre as modulo_nombre,
                       p.rol_id, r.nombre as rol_nombre, p.estado
                FROM permisos p
                JOIN modulos m ON p.modulo_id = m.id
                JOIN roles r ON p.rol_id = r.id
                WHERE p.deleted_at IS NULL
                ORDER BY r.nombre, m.nombre
            """)
            
            result = cursor.fetchall()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontraron permisos"
                )
                
            return {"permisos": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al listar permisos: {err}"
            )
        finally:
            conn.close()

    def obtener_permiso(self, permiso_id: int) -> dict:
        """Obtiene un permiso específico por ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT p.id, p.modulo_id, m.nombre as modulo_nombre,
                       p.rol_id, r.nombre as rol_nombre, p.estado
                FROM permisos p
                JOIN modulos m ON p.modulo_id = m.id
                JOIN roles r ON p.rol_id = r.id
                WHERE p.id = %s AND p.deleted_at IS NULL
            """, (permiso_id,))
            
            result = cursor.fetchone()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Permiso no encontrado"
                )
                
            return {"permiso": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener permiso: {err}"
            )
        finally:
            conn.close()

    def actualizar_permiso(self, permiso_id: int, permiso: Permisos) -> dict:
        """Actualiza un permiso existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """UPDATE permisos SET
                    modulo_id = %s,
                    rol_id = %s,
                    estado = %s,
                    updated_at = NOW()
                WHERE id = %s""",
                (permiso.modulo_id, permiso.rol_id, permiso.estado, permiso_id)
            )
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Permiso no encontrado"
                )
                
            return {"resultado": "Permiso actualizado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al actualizar permiso: {err}"
            )
        finally:
            conn.close()

    def eliminar_permiso(self, permiso_id: int) -> dict:
        """Elimina lógicamente un permiso"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE permisos SET deleted_at = NOW() WHERE id = %s",
                (permiso_id,)
            )
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Permiso no encontrado"
                )
                
            return {"resultado": "Permiso eliminado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al eliminar permiso: {err}"
            )
        finally:
            conn.close()

    def listar_permisos_por_rol(self, rol_id: int) -> dict:
        """Obtiene todos los módulos permitidos para un rol"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT m.id, m.nombre, m.descripcion
                FROM permisos p
                JOIN modulos m ON p.modulo_id = m.id
                WHERE p.rol_id = %s 
                AND p.estado = 1 
                AND p.deleted_at IS NULL
            """, (rol_id,))
            
            result = cursor.fetchall()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontraron permisos para este rol"
                )
                
            return {"modulos": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al listar permisos: {err}"
            )
        finally:
            conn.close()

    def actualizar_permisos_rol(self, rol_id: int, permisos: List[Permisos]) -> dict:
        """Actualiza todos los permisos de un rol (reemplaza los existentes)"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar existencia del rol
            cursor.execute("SELECT 1 FROM roles WHERE id = %s", (rol_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Rol no encontrado")
            
            # Transacción para actualización masiva
            conn.start_transaction()
            
            # 1. Desactivar permisos existentes
            cursor.execute(
                "UPDATE permisos SET estado = 0 WHERE rol_id = %s",
                (rol_id,)
            )
            
            # 2. Activar/crear nuevos permisos
            for permiso in permisos:
                # Verificar existencia del módulo
                cursor.execute("SELECT 1 FROM modulos WHERE id = %s", (permiso.modulo_id,))
                if not cursor.fetchone():
                    conn.rollback()
                    raise HTTPException(status_code=400, detail=f"Módulo {permiso.modulo_id} no existe")
                
                cursor.execute("""
                    INSERT INTO permisos (modulo_id, rol_id, estado)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE estado = VALUES(estado)
                """, (permiso.modulo_id, rol_id, permiso.estado))
            
            conn.commit()
            return {"resultado": "Permisos actualizados exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al actualizar permisos: {err}"
            )
        finally:
            conn.close()