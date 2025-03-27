from fastapi import APIRouter
from controllers.historial_usuario_controller import HistorialUsuarioController
from models.historial_usuario_model import Historial_usuario

router = APIRouter()
historial_controller = HistorialUsuarioController()

@router.post("/create_historial")
async def create_historial(historial: Historial_usuario):
    rpta = historial_controller.create_historial(historial)
    return rpta

@router.get("/get_historial/{historial_id}", response_model=Historial_usuario)
async def get_historial(historial_id: int):
    rpta = historial_controller.get_historial(historial_id)
    return rpta

@router.get("/get_historiales")
async def get_historiales():
    rpta = historial_controller.get_historiales()
    return rpta

@router.put("/edit_historial/{historial_id}")
async def edit_historial(historial_id: int, historial: Historial_usuario):
    rpta = historial_controller.edit_historial(historial_id, historial)
    return rpta

@router.delete("/delete_historial/{historial_id}")
async def delete_historial(historial_id: int):
    rpta = historial_controller.delete_historial(historial_id)
    return rpta
