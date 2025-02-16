from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import aiofiles
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

file_path = "https://maicoder.f5.si/templates/problem/problem.html"

async def read_html_file(file_path: str) -> str:
    try:
        async with aiofiles.open(file_path, mode='r') as file:
            return await file.read()
    except FileNotFoundError:
        return "<h1>File not found</h1>"

@app.get("/contest/", response_class=HTMLResponse)
async def get_contest_page():
    content = await read_html_file(file_path)
    return HTMLResponse(content=content)

@app.get("/quiz/", response_class=HTMLResponse)
async def get_quiz_page():
    content = await read_html_file(file_path)
    return HTMLResponse(content=content)
