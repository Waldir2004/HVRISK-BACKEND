from fastapi import APIRouter
from controllers.parametros_valor_controller import ParametrosValorController
from models.parametros_valor_models import parametros_valor

router = APIRouter()
parametros_valor_controller = ParametrosValorController()

@router.post("/create_parametro_valor")
async def create_parametro_valor(parametro_valor: parametros_valor):
    rpta = parametros_valor_controller.create_parametro_valor(parametro_valor)
    return rpta

@router.get("/get_parametro_valor/{parametro_valor_id}", response_model=parametros_valor)
async def get_parametro_valor(parametro_valor_id: int):
    rpta = parametros_valor_controller.get_parametro_valor(parametro_valor_id)
    return rpta

@router.get("/get_parametros_valores")
async def get_parametros_valores():
    rpta = parametros_valor_controller.get_parametros_valores()
    return rpta

@router.put("/edit_parametro_valor/{parametro_valor_id}")
async def edit_parametro_valor(parametro_valor_id: int, parametro_valor: parametros_valor):
    rpta = parametros_valor_controller.edit_parametro_valor(parametro_valor_id, parametro_valor)
    return rpta

@router.delete("/delete_parametro_valor/{parametro_valor_id}")
async def delete_parametro_valor(parametro_valor_id: int):
    rpta = parametros_valor_controller.delete_parametro_valor(parametro_valor_id)
    return rpta

@router.get("/get_parametro_valor_por_parametro_id/{parametro_id}")
async def get_parametros_valor_por_parametro_id(parametro_id: int):
    rpta = parametros_valor_controller.get_parametros_valor_por_parametro_id(parametro_id)
    return rpta