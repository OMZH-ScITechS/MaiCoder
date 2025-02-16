from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import aiofiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/contest/{directory}", response_class=HTMLResponse)
async def get_contest_page(directory: str):
    file_path = f"templates/contest/{directory}.html"
    async with aiofiles.open(file_path, mode='r') as file:
        content = await file.read()
    return HTMLResponse(content=content)

@app.get("/quiz/{directory}", response_class=HTMLResponse)
async def get_quiz_page(directory: str):
    file_path = f"templates/quiz/{directory}.html"
    async with aiofiles.open(file_path, mode='r') as file:
        content = await file.read()
    return HTMLResponse(content=content)
