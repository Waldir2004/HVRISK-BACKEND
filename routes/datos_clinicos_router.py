from fastapi import APIRouter, HTTPException
from controllers.datos_clinicos_controller import DatosClinicosController
from models.datos_clinicos_model import DatosClinicos
from typing import Optional

router = APIRouter(
    prefix="/datos-clinicos",
    tags=["Datos Clínicos"],
    responses={404: {"description": "No encontrado"}}
)

controller = DatosClinicosController()

@router.post("/crear", response_model=dict, status_code=201)
async def crear_datos(datos: DatosClinicos):
    """Registra nuevos datos clínicos"""
    return controller.crear_datos_clinicos(datos)

@router.get("/listar", response_model=dict)
async def listar_datos(paciente_id: Optional[int] = None):
    """Lista datos clínicos (filtra por paciente_id si se provee)"""
    return controller.listar_datos_clinicos(paciente_id)

@router.get("/obtener/{datos_id}", response_model=dict)
async def obtener_datos(datos_id: int):
    """Obtiene datos clínicos por ID"""
    return controller.obtener_datos_clinicos(datos_id)

@router.put("/actualizar/{datos_id}", response_model=dict)
async def actualizar_datos(datos_id: int, datos: DatosClinicos):
    """Actualiza datos clínicos existentes"""
    return controller.actualizar_datos_clinicos(datos_id, datos)

@router.delete("/eliminar/{datos_id}", response_model=dict)
async def eliminar_datos(datos_id: int):
    """Elimina lógicamente un registro"""
    return controller.eliminar_datos_clinicos(datos_id)