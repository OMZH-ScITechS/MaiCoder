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

@app.get("/api/judge/wandbox")
async def root(code: str = '',compiler: str = '',stdin: str = ''):
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

    return {"message": result, "speed": ut-time.time()}

def main():
    uvicorn.run("project_name.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()