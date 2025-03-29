import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.estilo_vida_model import EstiloVida
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from datetime import datetime

class EstiloVidaController:
    def create_estilo_vida(self, estilo: EstiloVida) -> dict:
        """Crea un nuevo registro de estilo de vida"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO estilo_vida (
                    paciente_id, actividad_fisica_id, 
                    consumo_alcohol_id, dieta_alta_sodio
                ) VALUES (%s, %s, %s, %s)
            """
            values = (
                estilo.paciente_id,
                estilo.actividad_fisica_id,
                estilo.consumo_alcohol_id,
                estilo.dieta_alta_sodio
            )
            
            cursor.execute(query, values)
            conn.commit()
            return {
                "resultado": "Registro de estilo de vida creado",
                "id": cursor.lastrowid
            }
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500, 
                detail=f"Error al crear registro: {err}"
            )
        finally:
            conn.close()

    def get_estilos_vida(self, paciente_id: Optional[int] = None) -> List[dict]:
        """Obtiene registros de estilo de vida, con filtro opcional por paciente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM estilo_vida WHERE deleted_at IS NULL"
            if paciente_id:
                query += " AND paciente_id = %s"
                cursor.execute(query, (paciente_id,))
            else:
                cursor.execute(query)
                
            result = cursor.fetchall()
            if not result:
                raise HTTPException(
                    status_code=404, 
                    detail="No se encontraron registros"
                )
                
            return {"resultado": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500, 
                detail=f"Error al obtener registros: {err}"
            )
        finally:
            conn.close()

    def get_estilo_vida_by_id(self, estilo_id: int) -> dict:
        """Obtiene un registro específico por ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT * FROM estilo_vida WHERE id = %s AND deleted_at IS NULL",
                (estilo_id,)
            )
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(
                    status_code=404, 
                    detail="Registro no encontrado"
                )
                
            return {"resultado": jsonable_encoder(result)}
            
        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500, 
                detail=f"Error al obtener registro: {err}"
            )
        finally:
            conn.close()

    def update_estilo_vida(self, estilo_id: int, estilo: EstiloVida) -> dict:
        """Actualiza un registro existente"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE estilo_vida SET
                    paciente_id = %s,
                    actividad_fisica_id = %s,
                    consumo_alcohol_id = %s,
                    dieta_alta_sodio = %s,
                    updated_at = NOW()
                WHERE id = %s
            """
            values = (
                estilo.paciente_id,
                estilo.actividad_fisica_id,
                estilo.consumo_alcohol_id,
                estilo.dieta_alta_sodio,
                estilo_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, 
                    detail="Registro no encontrado"
                )
                
            return {"resultado": "Registro actualizado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500, 
                detail=f"Error al actualizar: {err}"
            )
        finally:
            conn.close()

    def delete_estilo_vida(self, estilo_id: int) -> dict:
        """Elimina lógicamente un registro"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE estilo_vida SET deleted_at = NOW() WHERE id = %s",
                (estilo_id,)
            )
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, 
                    detail="Registro no encontrado"
                )
                
            return {"resultado": "Registro eliminado exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500, 
                detail=f"Error al eliminar: {err}"
            )
        finally:
            conn.close()