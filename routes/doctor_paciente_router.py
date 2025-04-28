from fastapi import APIRouter, Depends
from controllers.doctor_paciente_controller import DoctorPacienteController
from models.doctor_paciente_model import DoctorPacienteCreate
from typing import List
from config.bd_config import get_db_connection

router = APIRouter()
controller = DoctorPacienteController()

@router.post("/doctor-paciente", tags=["Doctor-Paciente"])
def crear_relacion_doctor_paciente(relacion: DoctorPacienteCreate):
    return controller.asignar_doctor_paciente(relacion)