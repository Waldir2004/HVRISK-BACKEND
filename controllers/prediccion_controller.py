import mysql.connector
from fastapi import HTTPException
from config.bd_config import get_db_connection
from models.prediccion_model import prediccion
from fastapi.encoders import jsonable_encoder

class prediccionController:
    def __init__(self, service):
        self.service = service

    def create_prediccion(self, prediccion):
        return self.service.create_prediccion(prediccion)

class PrediccionService:
    def create_prediccion(self, prediccion):
        # Lógica para calcular IMC
        altura_m = prediccion.altura_cm / 100
        imc = prediccion.peso_kg / (altura_m ** 2)

        # Calcular nivel de riesgo
        riesgo = self.calcular_riesgo(imc, prediccion)

        # Obtener recomendaciones basadas en el nivel de riesgo
        recomendaciones = self.obtener_recomendaciones(riesgo)

        # Retornar resultado
        return {
            "mensaje": f"El riesgo de enfermedad cardiovascular es {riesgo}",
            "recomendaciones": recomendaciones
        }

    def calcular_riesgo(self, imc, datos):
        # Ponderaciones para riesgo basado en factores comunes
        riesgo = 0
        if imc >= 30:
            riesgo += 2  # Obesidad
        elif imc >= 25:
            riesgo += 1  # Sobrepeso

        if datos.presion_sistolica > 140 or datos.presion_diastolica > 90:
            riesgo += 2

        if datos.colesterol == 6:
            riesgo += 2

        if datos.glucosa == 6:
            riesgo += 2

        if datos.fuma:
            riesgo += 1

        if datos.alcohol:
            riesgo += 1

        if not datos.dieta:
            riesgo += 1

        if not datos.actividad_fisica:
            riesgo += 1

        if datos.antecedentes_familiares:
            riesgo += 2

        if datos.diabetes:
            riesgo += 2

        # Evaluar nivel de riesgo
        if riesgo >= 8:
            return 'alto'
        elif 4 <= riesgo < 8:
            return 'medio'
        else:
            return 'bajo'

    def obtener_recomendaciones(self, riesgo):
        if riesgo == 'alto':
            return [
                "Consulta a un médico especialista para un plan de tratamiento personalizado.",
                "Realiza ejercicio físico moderado al menos 30 minutos al día, cinco veces a la semana.",
                "Adopta una dieta rica en frutas, verduras, granos enteros y proteínas magras.",
                "Evita completamente el consumo de tabaco y limita el consumo de alcohol.",
                "Monitorea regularmente tu presión arterial, niveles de glucosa y colesterol.",
                "Considera la posibilidad de unirte a un grupo de apoyo para mantener la motivación."
            ]
        elif riesgo == 'medio':
            return [
                "Programa chequeos médicos cada seis meses para monitorear tu salud.",
                "Incrementa tu actividad física diaria, incluyendo ejercicios cardiovasculares y de fuerza.",
                "Sigue una dieta balanceada, reduciendo el consumo de grasas saturadas y azúcares.",
                "Limita el consumo de tabaco y alcohol, buscando ayuda profesional si es necesario.",
                "Mantén un peso saludable y controla tu índice de masa corporal (IMC).",
                "Practica técnicas de manejo del estrés como la meditación o el yoga."
            ]
        else:
            return [
                "Mantén un estilo de vida saludable con una dieta equilibrada y ejercicio regular.",
                "Realiza al menos 150 minutos de actividad física moderada a la semana.",
                "Incluye en tu dieta alimentos ricos en fibra, vitaminas y minerales.",
                "Evita el consumo excesivo de alcohol y no fumes.",
                "Realiza chequeos médicos anuales para prevenir posibles problemas de salud.",
                "Fomenta hábitos de sueño saludables, asegurándote de dormir entre 7 y 9 horas por noche."
            ]
#     def create_prediccion(self, prediccion: prediccion):   
#         try:
#             conn = get_db_connection()
#             cursor = conn.cursor()
#             cursor.execute("""
#     INSERT INTO predicciones (id, usuario_id, edad, genero, altura_cm, peso_kg, presion_sistolica, presion_diastolica, colesterol, glucosa, fuma, alcohol, dieta, actividad_fisica, antecedentes_familiares, diabetes, prediccion_riesgo, estado)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
# """, (
#     prediccion.id, prediccion.usuario_id, prediccion.edad, prediccion.genero,
#     prediccion.altura_cm, prediccion.peso_kg, prediccion.presion_sistolica,
#     prediccion.presion_diastolica, prediccion.colesterol, prediccion.glucosa,
#     prediccion.fuma, prediccion.alcohol, prediccion.dieta, prediccion.actividad_fisica,
#     prediccion.antecedentes_familiares, prediccion.diabetes, prediccion.prediccion_riesgo,
#     prediccion.estado
# ))

#             conn.commit()
#             return {"resultado": "prediccion creado"}
#         except mysql.connector.Error as err:
#             conn.rollback()
#             raise HTTPException(status_code=500, detail=str(err))
#         finally:
#             conn.close()
    
#     def get_prediccion_by_id(self, prediccion_id: int):
#         try:
#             conn = get_db_connection()
#             cursor = conn.cursor(dictionary=True)
#             cursor.execute("SELECT * FROM predicciones WHERE id = %s", (prediccion_id,))
#             result = cursor.fetchone()

#             if not result:
#                 raise HTTPException(status_code=404, detail="Predicción no encontrada")

#             return result
#         except mysql.connector.Error as err:
#             raise HTTPException(status_code=500, detail=str(err))
#         finally:
#             conn.close()

#     def get_all_predicciones(self):
#         try:
#             conn = get_db_connection()
#             cursor = conn.cursor(dictionary=True)
#             cursor.execute("SELECT * FROM predicciones")
#             results = cursor.fetchall()

#             if not results:
#                 raise HTTPException(status_code=404, detail="No se encontraron predicciones")

#             return results
#         except mysql.connector.Error as err:
#             raise HTTPException(status_code=500, detail=str(err))
#         finally:
#             conn.close()