from fastapi import APIRouter
from controllers.parametros_controller import ParametrosController
from models.parametros_models import parametros

router = APIRouter()
parametros_controller = ParametrosController()

@router.post("/create_parametro")
async def create_parametro(parametro: parametros):
    rpta = parametros_controller.create_parametro(parametro)
    return rpta

@router.get("/get_parametro/{parametro_id}", response_model=parametros)
async def get_parametro(parametro_id: int):
    rpta = parametros_controller.get_parametro(parametro_id)
    return rpta

@router.get("/get_parametros")
async def get_parametros():
    rpta = parametros_controller.get_parametros()
    return rpta

@router.put("/edit_parametro/{parametro_id}")
async def edit_parametro(parametro_id: int, parametro: parametros):
    rpta = parametros_controller.edit_parametro(parametro_id, parametro)
    return rpta

@router.delete("/delete_parametro/{parametro_id}")
async def delete_parametro(parametro_id: int):
    rpta = parametros_controller.delete_parametro(parametro_id)
    return rpta
