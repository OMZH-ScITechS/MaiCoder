from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import requests

router = APIRouter()
problems_dir = "/app/data/contests/"

@router.get("/{subpath:path}", response_class=HTMLResponse)
async def get_contest_page(subpath: str):
    try:
        response = requests.get('https://maicoder.f5.si/templates/contest/contest.html')
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        content = response.text
    except requests.HTTPError:
        content = "<h1>Failed to fetch content</h1>"
    return HTMLResponse(content=content)
