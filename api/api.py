from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import json
import time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"]
)

@app.post("/judge/test")
async def root(request: Request):
    ut = float(time.time())
    
    data = await request.json()
    code = data.get('code', 'print("hello world")')
    compiler = data.get('compiler', 'pypy-3.7-v7.3.9')
    stdin = data.get('stdin', '')

    url = "https://wandbox.org/api/compile.json"
    payload = {
        "code": code,
        "compiler": compiler,
        "stdin": stdin
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        result = response.json()
    else:
        result = 'Error'

    return {"message": result, "speed": time.time()-ut}
