from fastapi import APIRouter, Request
import os
import json
from datetime import datetime

router = APIRouter()
contests_dir = "/app/data/contests/"

@router.get("/{subpath:path}")
async def get_contest_datail(subpath: str):
    try:
        with open(f"{contests_dir}{subpath}.json", "r") as file:
            content = json.load(file)
            contest_date = datetime.fromisoformat(content.get("date"))
            if contest_date > datetime.now():
                del content["problems"]
        return content
    except FileNotFoundError:
        return {"error": "File not found"}, 404
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}, 400
    except Exception as e:
        return {"error": str(e)}, 500

@router.post("/post")
async def post_contest(request: Request):
    try:
        data = await request.json()

        contest_id = data.name.lower()
        
        with open(f"{contests_dir}{contest_id}.json", "w") as file:
            json.dump(data, file)
        
        return {"contest_id": contest_id}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}, 400
    except Exception as e:
        return {"error": str(e)}, 500