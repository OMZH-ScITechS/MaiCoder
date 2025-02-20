from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse  # Add this import
import uvicorn
import requests
import json
import time
import os  # Add this import

problems_dir = "/app/data/problems/"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"]
)

$async def fetch_html_content() -> str:
    try:
        response = requests.get('https://maicoder.f5.si/templates/problem/problem.html')
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except requests.HTTPError:
        return "<h1>Failed to fetch content</h1>"

#@app.get("/contest/{subpath:path}", response_class=HTMLResponse)
#async def get_contest_page(subpath: str):
#    content = await fetch_html_content()
#    return HTMLResponse(content=content)

#@app.get("/problems/{subpath:path}", response_class=HTMLResponse)
#async def get_quiz_page(subpath: str):
#    content = await fetch_html_content()
#    return HTMLResponse(content=content)


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

@app.get("/problems/{subpath:path}")
async def get_problems(subpath: str):
    try:
        with open(f"{problems_dir}{subpath}.json", "r") as file:
            content = json.load(file)
            del content["tests"]
        return content
    except FileNotFoundError:
        return {"error": "File not found"}, 404
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}, 400
    except Exception as e:
        return {"error": str(e)}, 500

@app.post("/problems/post")
async def post_problem(request: Request):
    try:
        data = await request.json()

        existing_files = [f for f in os.listdir(problems_dir) if f.endswith(".json")]
        problem_id = str(len(existing_files) + 1).zfill(5)
        
        with open(f"{problems_dir}{problem_id}.json", "w") as file:
            json.dump(data, file)
        
        return {"problem_id": problem_id}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}, 400
    except Exception as e:
        return {"error": str(e)}, 500