from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import requests
import markdown

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

def embed_markdown(html_content: str, markdown_content: str) -> str:
    md_html = markdown.markdown(markdown_content)
    start_tag = f'<div id="content">'
    end_tag = '</div>'
    start_index = html_content.find(start_tag) + len(start_tag)
    end_index = html_content.find(end_tag, start_index)
    if start_index != -1 and end_index != -1:
        return html_content[:start_index] + md_html + html_content[end_index:]
    return html_content

@app.get("/contest/{subpath:path}", response_class=HTMLResponse)
async def get_contest_page(subpath: str):
    html_content = await fetch_html_content(file_url)
    markdown_content = "# Contest Page\nThis is a contest page."
    content = embed_markdown(html_content, markdown_content)
    return HTMLResponse(content=content)

@app.get("/quiz/{subpath:path}", response_class=HTMLResponse)
async def get_quiz_page(subpath: str):
    html_content = await fetch_html_content(file_url)
    markdown_content = "# Quiz Page\nThis is a quiz page."
    content = embed_markdown(html_content, markdown_content)
    return HTMLResponse(content=content)
