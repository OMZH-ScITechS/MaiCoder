from fastapi import FastAPI
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

@app.get("/judge/test")
async def root(code: str = 'print("hello world")',compiler: str = 'pypy-3.7-v7.3.9',stdin: str = ''):
    ut = float(time.time())
    
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
