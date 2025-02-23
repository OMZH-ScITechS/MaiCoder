from fastapi import APIRouter, Request
import os
import json

router = APIRouter()
problems_dir = "/app/data/contests/"

@router.get("/{subpath:path}")
async def get_contest_datail(subpath: str):
    try:
        with open(f"{problems_dir}{subpath}.json", "r") as file:
            content = json.load(file)
        return content
    except FileNotFoundError:
        return {"error": "File not found"}, 404
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}, 400
    except Exception as e:
        return {"error": str(e)}, 500