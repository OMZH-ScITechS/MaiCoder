from fastapi import APIRouter, Request
import os
import json
from datetime import datetime

router = APIRouter()
problems_dir = "/app/data/problems/"

@router.get("/{subpath:path}")
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

@router.post("/post")
async def post_problem(request: Request):
    try:
        data = await request.json()
        
        problem_date = datetime.fromisoformat(data.get("date"))
        if problem_date > datetime.now():
            return {"error": "This problem has not been published"}, 400

        existing_files = [f for f in os.listdir(problems_dir) if f.endswith(".json")]
        problem_id = str(len(existing_files) + 1).zfill(5)
        
        with open(f"{problems_dir}{problem_id}.json", "w") as file:
            json.dump(data, file)
        
        return {"problem_id": problem_id}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}, 400
    except Exception as e:
        return {"error": str(e)}, 500