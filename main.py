from fastapi import FastAPI
from routes.user_router import router as user_router
from routes.roles_router import router as roles_router 
from routes.parametros_valor_router import router as parametros_valor_router
from routes.parametros_router import router as parametros_router
from routes.modulos_router import router as modulos_router
from routes.auth_routes import router as auth_router
from routes.permisos_router import router as permisos_router
from routes.antecedentes_router import router as antecedentes_router
from routes.datos_clinicos_router import router as datos_clinicos_router
from routes.estilo_vida_router import router as estilo_vida_router
from routes.evaluaciones_router import router as evaluaciones_router
from routes.doctor_paciente_router import router as doctor_paciente_router
from routes.evaluaciones_completas_router import router as evaluaciones_completas_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(roles_router)
app.include_router(parametros_valor_router)
app.include_router(parametros_router)
app.include_router(modulos_router)
app.include_router(auth_router)
app.include_router(permisos_router)
app.include_router(antecedentes_router)
app.include_router(datos_clinicos_router)
app.include_router(estilo_vida_router)
app.include_router(evaluaciones_router)
app.include_router(doctor_paciente_router)
app.include_router(evaluaciones_completas_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)