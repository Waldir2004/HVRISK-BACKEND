from fastapi import APIRouter
from controllers.enfermedades_controller import EnfermedadesController
from models.enfermedades_models import enfermedades

router = APIRouter()
enfermedades_controller = EnfermedadesController()

@router.post("/create_enfermedad")
async def create_enfermedad(enfermedad: enfermedades):
    rpta = enfermedades_controller.create_enfermedad(enfermedad)
    return rpta

@router.get("/get_enfermedad/{enfermedad_id}", response_model=enfermedades)
async def get_enfermedad(enfermedad_id: int):
    rpta = enfermedades_controller.get_enfermedad(enfermedad_id)
    return rpta

@router.get("/get_enfermedades")
async def get_enfermedades():
    rpta = enfermedades_controller.get_enfermedades()
    return rpta

@router.put("/edit_enfermedad/{enfermedad_id}")
async def edit_enfermedad(enfermedad_id: int, enfermedad: enfermedades):
    rpta = enfermedades_controller.edit_enfermedad(enfermedad_id, enfermedad)
    return rpta

@router.delete("/delete_enfermedad/{enfermedad_id}")
async def delete_enfermedad(enfermedad_id: int):
    rpta = enfermedades_controller.delete_enfermedad(enfermedad_id)
    return rpta
