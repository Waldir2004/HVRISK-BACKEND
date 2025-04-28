from pydantic import BaseModel
from datetime import datetime

class DoctorPacienteBase(BaseModel):
    doctor_id: int
    paciente_id: int

class DoctorPacienteCreate(DoctorPacienteBase):
    pass

class DoctorPaciente(DoctorPacienteBase):
    id: int
    fecha_asignacion: datetime

    class Config:
        from_attributes = True