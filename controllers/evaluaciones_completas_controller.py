from fastapi import HTTPException
from typing import Dict, Any
from datetime import datetime
from models.evaluaciones_model import Evaluaciones
from models.datos_clinicos_model import DatosClinicos
from models.antecedentes_model import Antecedentes
from models.estilo_vida_model import EstiloVida
from controllers.evaluaciones_controller import EvaluacionesController
from controllers.datos_clinicos_controller import DatosClinicosController
from controllers.antecedentes_controller import AntecedentesController
from controllers.estilo_vida_controller import EstiloVidaController

class EvaluacionesCompletasController:

    def __init__(self):
        self.controller_eval = EvaluacionesController()
        self.controller_clinicos = DatosClinicosController()
        self.controller_antecedentes = AntecedentesController()
        self.controller_estilo = EstiloVidaController()

    def crear_evaluacion_completa(self, datos: dict):
        try:
            # Crear evaluación
            eval_data = {
                "paciente_id": datos["pacienteAsignado"],
                "fecha_evaluacion": datetime.now(),
                "riesgo_hvi_id": None,
                "riesgo_hvd_id": None,
                "puntuacion_hvi": None,
                "puntuacion_hvd": None,
                "framingham_risk": None,
                "notas": None
            }
            evaluacion = self.controller_eval.create_evaluacion(Evaluaciones(**eval_data))
            eval_id = evaluacion["id"]

            # Crear datos clínicos
            clinicos_data = {
                "evaluacion_id": eval_id,
                "peso_kg": datos["peso_kg"],
                "altura_cm": datos["altura_cm"],
                "circ_cintura_cm": datos["circ_cintura_cm"],
                "presion_sistolica": datos["presion_sistolica"],
                "presion_diastolica": datos["presion_diastolica"],
                "frecuencia_cardiaca": datos["frecuencia_cardiaca"],
                "ldl": datos["ldl"],
                "hdl": datos["hdl"],
                "trigliceridos": datos["trigliceridos"],
                "glucosa_ayunas": datos["glucosa_ayunas"],
                "hba1c": datos["hba1c"],
                "creatinina": datos["creatinina"]
            }
            clinicos = self.controller_clinicos.create_datos_clinicos(DatosClinicos(**clinicos_data))

            # Crear antecedentes
            antecedentes_data = {
                "evaluacion_id": eval_id,
                "diabetes": datos["diabetes"],
                "hipertension": datos["hipertension"],
                "enfermedad_renal": datos["enfermedad_renal"],
                "apnea_sueno": datos["apnea_sueno"],
                "dislipidemia": datos["dislipidemia"],
                "epoc": datos["epoc"],
                "familia_cardiopatia": datos["familia_cardiopatia"],
                "familia_diabetes": datos["familia_diabetes"],
                "tabaquismo_id": datos["tabaquismo_id"]
            }
            antecedentes = self.controller_antecedentes.create_antecedente(Antecedentes(**antecedentes_data))

            # Crear estilo de vida
            estilo_data = {
                "evaluacion_id": eval_id,
                "actividad_fisica_id": datos["actividad_fisica_id"],
                "horas_ejercicio_semana": datos["horas_ejercicio_semana"],
                "consumo_alcohol_id": datos["consumo_alcohol_id"],
                "consumo_cafeina_id": datos["consumo_cafeina_id"],
                "dieta_alta_sodio": datos["dieta_alta_sodio"],
                "dieta_alta_grasas": datos["dieta_alta_grasas"],
                "horas_sueno_diario": datos["horas_sueno_diario"],
                "calidad_sueno_id": datos["calidad_sueno_id"],
                "nivel_estres_id": datos["nivel_estres_id"]
            }
            estilo = self.controller_estilo.create_estilo_vida(EstiloVida(**estilo_data))

            return {
                "success": True,
                "evaluacion_id": eval_id,
                "datos_clinicos_id": clinicos["id"],
                "antecedentes_id": antecedentes["id"],
                "estilo_vida_id": estilo["id"]
            }

        except Exception as e:
            raise Exception(f"Error en registro completo: {str(e)}")