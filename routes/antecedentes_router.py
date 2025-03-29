from fastapi import APIRouter, HTTPException
from controllers.antecedentes_controller import AntecedentesController
from models.antecedentes_model import Antecedentes
from typing import Optional

router = APIRouter(
    prefix="/antecedentes",
    tags=["Antecedentes Médicos"],
    responses={404: {"description": "No encontrado"}}
)

controller = AntecedentesController()

@router.post("/crear", response_model=dict, status_code=201)
async def crear_antecedente(antecedente: Antecedentes):
    """Crea un nuevo registro de antecedentes médicos"""
    return controller.create_antecedente(antecedente)

@router.get("/listar", response_model=dict)
async def listar_antecedentes(evaluation_id: Optional[int] = None):
    """Obtiene todos los antecedentes o filtra por evaluation_id"""
    return controller.get_antecedentes(evaluation_id)

@router.get("/obtener/{antecedente_id}", response_model=dict)
async def obtener_antecedente(antecedente_id: int):
    """Obtiene un antecedente específico por ID"""
    return controller.get_antecedente(antecedente_id)

@router.put("/actualizar/{antecedente_id}", response_model=dict)
async def actualizar_antecedente(antecedente_id: int, antecedente: Antecedentes):
    """Actualiza un antecedente existente"""
    return controller.update_antecedente(antecedente_id, antecedente)

@router.delete("/eliminar/{antecedente_id}", response_model=dict)
async def eliminar_antecedente(antecedente_id: int):
    """Elimina lógicamente un antecedente"""
    return controller.delete_antecedente(antecedente_id)