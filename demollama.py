from fastapi import FastAPI, HTTPException
from pdfprocessor import extractTextFromPdf, convertToJson
import json
import ollama

app = FastAPI()

@app.get("/")
def readRoot():
    return {"mensaje": "La API está en funcionamiento"}

@app.post("/generate-health-report")
async def generateHealthReport(file_name: str):
    try:
        # 1. Extraer el texto usando tu módulo en inglés
        raw_text = extractTextFromPdf(file_name)
        
        # 2. Configurar el Prompt en español para el análisis
        # Limitamos a 6000 caracteres para optimizar el rendimiento del modelo 1b
        analysis_prompt = (
            f"Contexto: El siguiente texto proviene de un documento oficial de salud (ASIS Colombia). "
            f"Tarea: Actúa como un analista de datos experto. Genera un reporte estadístico sobre los "
            f"posibles problemas de salud en Colombia para el año 2025 basándote ÚNICAMENTE en esta información. "
            f"Incluye frecuencias estimadas o porcentajes si los datos lo permiten. "
            f"Contenido del texto: {raw_text[:6000]}"
        )

        # 3. Llamada a Ollama con instrucciones en español
        response = ollama.chat(
            model='llama3.2:1b',
            messages=[
                {
                    'role': 'system', 
                    'content': 'Eres un analista médico profesional. Proporcionas reportes estructurados con estadísticas y proyecciones de salud claras en español.'
                },
                {'role': 'user', 'content': analysis_prompt},
            ]
        )

        # 4. Respuesta de la API con claves en español dentro del JSON
        return {
            "estado": "exitoso",
            "archivo_origen": file_name,
            "reporte_analitico": response['message']['content']
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Archivo no encontrado: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Interno: {str(e)}")

@app.post("/process-local-pdf")
async def processPdf(file_name: str):
    try:
        raw_text = extractTextFromPdf(file_name)
        json_string = convertToJson(raw_text, file_name)
        structured_data = json.loads(json_string)
        
        return {
            "estado": "exitoso", 
            "datos_estructurados": structured_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

