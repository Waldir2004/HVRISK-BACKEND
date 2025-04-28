from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.doctor_paciente_model import DoctorPacienteCreate, DoctorPaciente
import mysql.connector

class DoctorPacienteController:
    
    def asignar_doctor_paciente(self, relacion: DoctorPacienteCreate) -> dict:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar que ambos usuarios existen
            cursor.execute("SELECT id, rol_id FROM usuarios WHERE id = %s", (relacion.doctor_id,))
            doctor = cursor.fetchone()
            if not doctor:
                raise HTTPException(status_code=404, detail="Doctor no encontrado")
            
            cursor.execute("SELECT id, rol_id FROM usuarios WHERE id = %s", (relacion.paciente_id,))
            paciente = cursor.fetchone()
            if not paciente:
                raise HTTPException(status_code=404, detail="Paciente no encontrado")
            
            # Verificar roles
            if doctor[1] != 2:  # 2 = Doctor
                raise HTTPException(status_code=400, detail="El usuario doctor no tiene el rol correcto")
            
            if paciente[1] != 3:  # 3 = Paciente
                raise HTTPException(status_code=400, detail="El usuario paciente no tiene el rol correcto")
            
            # Verificar si la relación ya existe
            cursor.execute("SELECT 1 FROM doctor_paciente WHERE doctor_id = %s AND paciente_id = %s", 
                          (relacion.doctor_id, relacion.paciente_id))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Esta relación doctor-paciente ya existe")
            
            # Crear la relación
            query = """
                INSERT INTO doctor_paciente (doctor_id, paciente_id)
                VALUES (%s, %s)
            """
            cursor.execute(query, (relacion.doctor_id, relacion.paciente_id))
            conn.commit()
            
            return {"mensaje": "Relación doctor-paciente creada exitosamente"}
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear relación doctor-paciente: {err}"
            )
        finally:
            conn.close()