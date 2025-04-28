from fastapi import APIRouter, HTTPException
from controllers.user_controller import UsuariosController
from models.user_models import Usuario
from typing import Optional

router = APIRouter(
    prefix="/usuarios",
    tags=["Gestión de Usuarios"],
    responses={
        404: {"description": "Usuario no encontrado"},
        400: {"description": "Solicitud inválida"},
        500: {"description": "Error interno del servidor"}
    }
)

controller = UsuariosController()

@router.post("/crear", response_model=dict, status_code=201)
async def crear_usuario(usuario: Usuario):
    """
    Registra un nuevo usuario en el sistema.
    
    Campos requeridos:
    - rol_id (int)
    - correo_electronico (string, formato email)
    - contraseña (string, min 8 caracteres)
    - nombre (string)
    - apellido (string)
    - tipo_identificacion (int)
    - numero_identificacion (string)
    """
    return controller.crear_usuario(usuario)

@router.get("/listar", response_model=dict)
async def listar_usuarios():
    """Obtiene todos los usuarios activos con información relacionada"""
    return controller.listar_usuarios()

@router.get("/por-rol/{rol_id}", response_model=dict)
async def listar_usuarios_por_rol(rol_id: int):
    return controller.listar_usuarios_por_rol(rol_id)

@router.get("/pacientes/por-doctor/{doctor_id}", response_model=dict)
async def listar_pacientes_por_doctor(doctor_id: int):
    return controller.listar_pacientes_por_doctor(doctor_id)

@router.get("/obtener/{usuario_id}", response_model=dict)
async def obtener_usuario(usuario_id: int):
    """Obtiene un usuario específico por su ID"""
    return controller.obtener_usuario(usuario_id)

@router.put("/actualizar/{usuario_id}", response_model=dict)
async def actualizar_usuario(usuario_id: int, usuario: Usuario):
    """Actualiza los datos de un usuario existente"""
    return controller.actualizar_usuario(usuario_id, usuario)

@router.delete("/eliminar/{usuario_id}", response_model=dict)
async def eliminar_usuario(usuario_id: int):
    """Elimina lógicamente un usuario (soft delete)"""
    return controller.eliminar_usuario(usuario_id)