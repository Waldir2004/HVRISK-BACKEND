from fastapi import APIRouter
from controllers.modulos_controller import ModulosController
from models.modulos_models import modulos

router = APIRouter()
modulos_controller = ModulosController()

@router.post("/create_modulo")
async def create_modulo(modulo: modulos):
    rpta = modulos_controller.create_modulo(modulo)
    return rpta

@router.get("/get_modulo/{modulo_id}", response_model=modulos)
async def get_modulo(modulo_id: int):
    rpta = modulos_controller.get_modulo(modulo_id)
    return rpta

@router.get("/get_modulos")
async def get_modulos():
    rpta = modulos_controller.get_modulos()
    return rpta

@router.put("/edit_modulo/{modulo_id}")
async def edit_modulo(modulo_id: int, modulo: modulos):
    rpta = modulos_controller.edit_modulo(modulo_id, modulo)
    return rpta

@router.delete("/delete_modulo/{modulo_id}")
async def delete_modulo(modulo_id: int):
    rpta = modulos_controller.delete_modulo(modulo_id)
    return rpta
