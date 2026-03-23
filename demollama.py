from fastapi import FastAPI, HTTPException
from pdfprocessor import extractTextFromPdf, convertToJson
import json

app = FastAPI()

@app.get("/")
def readRoot():
    return {"message":"API is running"}

@app.post("/process-local-pdf")
async def processPdf(file_name: str):
    try:
        raw_text = extractTextFromPdf(file_name)
        
        json_string = convertToJson(raw_text, file_name)
        structured_data = json.loads(json_string)
        
        return {
            "status": "success",
            "data": structured_data
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")
    
