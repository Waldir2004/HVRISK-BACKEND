from fastapi import APIRouter, HTTPException
from controllers.prediccion_controller import prediccionController, PrediccionService
from models.prediccion_model import prediccion

router = APIRouter()

# Crear una instancia de PrediccionService
service = PrediccionService()

# Pasar la instancia de servicio al controlador
controller = prediccionController(service=service)

@router.post("/create_prediccion")
async def create_prediccion(prediccion: prediccion):
    try:
        rpta = controller.create_prediccion(prediccion)
        return rpta
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.get("/get_prediccion/{prediccion_id}")
# async def get_prediccion(prediccion_id: int):
#     try:
#         rpta = controller.get_prediccion_by_id(prediccion_id)
#         return rpta
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/get_all_predicciones")
# async def get_all_prediccion():
#     try:
#         rpta = controller.get_all_predicciones()
#         return rpta
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
