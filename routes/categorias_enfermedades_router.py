from fastapi import APIRouter
from controllers.categorias_enfermedades_controller import CategoriasEnfermedadesController
from models.categorias_enfermedades_models import Categorias_enfermedades

router = APIRouter()
categorias_enfermedades_controller = CategoriasEnfermedadesController()

@router.post("/create_categoria")
async def create_categoria(categoria: Categorias_enfermedades):
    rpta = categorias_enfermedades_controller.create_categoria(categoria)
    return rpta

@router.get("/get_categoria/{categoria_id}", response_model=Categorias_enfermedades)
async def get_categoria(categoria_id: int):
    rpta = categorias_enfermedades_controller.get_categoria(categoria_id)
    return rpta

@router.get("/get_categorias")
async def get_categorias():
    rpta = categorias_enfermedades_controller.get_categorias()
    return rpta

@router.put("/edit_categoria/{categoria_id}")
async def edit_categoria(categoria_id: int, categoria: Categorias_enfermedades):
    rpta = categorias_enfermedades_controller.edit_categoria(categoria_id, categoria)
    return rpta

@router.delete("/delete_categoria/{categoria_id}")
async def delete_categoria(categoria_id: int):
    rpta = categorias_enfermedades_controller.delete_categoria(categoria_id)
    return rpta
