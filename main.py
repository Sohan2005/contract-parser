# main.py
# FastAPI application entry point
import json
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import shutil
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from app.pipeline import run_pipeline
from app.database import init_db, save_result, get_all_results, get_result_by_id
from app.errors import (
    EmptyDocumentError,
    PDFExtractionError,
    AIParsingError,
    FileTooLargeError
)

app = FastAPI(
    title="Contract Parser API",
    description="Upload a PDF contract and extract key entities using AI",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/app")
def serve_frontend():
    return FileResponse("static/index.html")

# Initialize database on startup
init_db()

@app.get("/")
def root():
    return {"message": "Contract Parser API is running"}

@app.post("/upload")
async def upload_contract(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(".pdf"):
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Invalid file type. Only PDF files are accepted."
            }
        )

    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = run_pipeline(temp_path)
        save_result(file.filename, result)
        return JSONResponse(content={
            "status": "success",
            "filename": file.filename,
            "data": result
        })

    except FileTooLargeError as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e)}
        )
    except EmptyDocumentError as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e)}
        )
    except PDFExtractionError as e:
        return JSONResponse(
            status_code=422,
            content={"status": "error", "message": str(e)}
        )
    except AIParsingError as e:
        return JSONResponse(
            status_code=502,
            content={"status": "error", "message": str(e)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "An unexpected error occurred. Please try again."
            }
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/contracts")
def get_contracts():
    rows = get_all_results()
    contracts = []
    for row in rows:
        contracts.append({
            "id": row[0],
            "filename": row[1],
            "contract_type": row[2],
            "effective_date": row[3],
            "created_at": row[4]
        })
    return {"status": "success", "contracts": contracts}

@app.get("/contracts/{doc_id}")
def get_contract(doc_id: int):
    row = get_result_by_id(doc_id)
    if not row:
        return JSONResponse(
            status_code=404,
            content={"status": "error", "message": "Contract not found"}
        )
    return {
        "status": "success",
        "data": {
            "id": row[0],
            "filename": row[1],
            "contract_type": row[2],
            "parties": json.loads(row[3]) if row[3] else [],
            "effective_date": row[4],
            "expiry_date": row[5],
            "dollar_amounts": json.loads(row[6]) if row[6] else [],
            "key_obligations": json.loads(row[7]) if row[7] else [],
            "termination_clause": row[8],
            "governing_law": row[9],
            "created_at": row[10]
        }
    }