from typing import Union
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from backend.rag_pipeline import *
import os

# use "uvicorn main:app --reload" to run the code.
app = FastAPI(title="RAG chat with Youtube transcript")


class QueryRequest(BaseModel):
   query: str

class IngestRequest(BaseModel):
   video_id: str

@app.get("/")
def read_root():
   return RedirectResponse('/docs')

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok", "message": "RAG backend running fine"}

@app.post("/ingest_video")
def transcript(req:IngestRequest):
   result = ingest_video(req.video_id)
   return {"message": "Video ingested successfully", "details": result}

@app.post("/query")
def query(req:QueryRequest):
   answer = retrieve_query_answer(req.query)
   return {"query": req.query, "answer": answer}


