from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

file_url = "https://maicoder.f5.si/templates/problem/problem.html"

async def fetch_html_content(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding  # Ensure correct encoding
        return response.text
    except requests.HTTPError:
        return "<h1>Failed to fetch content</h1>"

@app.get("/contest/{subpath:path}", response_class=HTMLResponse)
async def get_contest_page(subpath: str):
    content = await fetch_html_content(file_url)
    return HTMLResponse(content=content)

@app.get("/quiz/{subpath:path}", response_class=HTMLResponse)
async def get_quiz_page(subpath: str):
    content = await fetch_html_content(file_url)
    return HTMLResponse(content=content)
