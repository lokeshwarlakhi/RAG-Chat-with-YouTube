import os
from fastapi import FastAPI
from pydantic import BaseModel
from backend.rag_pipeline import *
from fastapi.responses import RedirectResponse

# use "uvicorn main:app --reload" to run the code.
app = FastAPI(title="RAG chat with Youtube transcript")


class QueryRequest(BaseModel):
    video_id: str
    query: str


class IngestRequest(BaseModel):
    video_id: str


@app.get("/")
async def read_root(): #there are no I/O operations in here, so wont make much of a difference in the execution.
    return RedirectResponse("/docs")


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok", "message": "RAG backend running fine"}


@app.post("/ingest_video")
async def transcript(req: IngestRequest):
    result = ingest_video(req.video_id)
    return {"message": "Video ingested successfully", "details": result}


@app.post("/query")
async def query(req: QueryRequest): # when query() is waiting, new requets can be accepted. 
    answer = await retrieve_query_answer(req.video_id, req.query)
    return {"video_id": req.video_id, "query": req.query, "answer": answer}
