import ollama
import fitz
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()

@app.get("/")
def read_root():
	return {"hello":"world"}

@app.post("/analtic")
async def analizer(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un pdf")

    try:
        pdf_content = await file.read()
        doc = fitz.open(stream=pdf_content, filetype="pdf")

        text_complete = ""
        for page in doc:
            text_complete += page.get_text()

        doc.close()

        prompt = (
            f"Actúa como un analista de datos experto. Basado en el siguiente texto extraído de un PDF, "
            f"genera un reporte que incluya probabilidades estadísticas o frecuencias sobre los temas principales. "
            f"Si no hay datos numéricos, estima la relevancia de los asuntos en porcentajes basándote en su mención. "
            f"Texto: {texto_completo[:4000]}" # Limitamos a 4000 caracteres por el contexto
        ) 
         response = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': 'Eres un asistente analítico que responde con datos y porcentajes.'},
            {'role': 'user', 'content': prompt},
        ])

        return {
            "archivo": file.filename,
            "analisis": response['message']['content']
        }

    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el PDF: {str(e)}"}

# Ejecución: uvicorn nombre_archivo:app --reload 

