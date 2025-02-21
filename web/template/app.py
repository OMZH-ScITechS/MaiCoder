from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
import requests

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"]
)

async def fetch_html_content() -> str:
    try:
        response = requests.get('https://maicoder.f5.si/templates/problem/problem.html')
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except requests.HTTPError:
        return "<h1>Failed to fetch content</h1>"

@app.get("/contests/{subpath:path}", response_class=HTMLResponse)
async def get_contest_page(subpath: str):
    content = await fetch_html_content()
    return HTMLResponse(content=content)

@app.get("/problems/{subpath:path}", response_class=HTMLResponse)
async def get_quiz_page(subpath: str):
    content = await fetch_html_content()
    return HTMLResponse(content=content)