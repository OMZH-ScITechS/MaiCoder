from fastapi import APIRouter, Request, HTTPException
import os
import json

router = APIRouter()
problems_dir = "/app/data/problems/"
submit_dir = "/app/data/submissions/"

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

@router.post("/submit/{subpath:path}")
async def submit_problem(subpath: str, request: Request):
    try:
        data = await request.json()

        # Ensure the submission directory exists
        os.makedirs(submit_dir + subpath, exist_ok=True)

        existing_files = [f for f in os.listdir(submit_dir + subpath) if f.endswith(".json")]
        submit_id = str(len(existing_files) + 1).zfill(5)
        
        with open(f"{submit_dir}{subpath}/{submit_id}.json", "w") as file:
            json.dump(data, file)
        
        # Process the submission (this is a placeholder, implement your logic here)
        result = {"status": "success", "submit_id": submit_id}
        
        return result
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

        existing_files = [f for f in os.listdir(problems_dir) if f.endswith(".json")]
        problem_id = str(len(existing_files) + 1).zfill(5)
        
        with open(f"{problems_dir}{problem_id}.json", "w") as file:
            json.dump(data, file)
        
        return {"problem_id": problem_id}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}, 400
    except Exception as e:
        return {"error": str(e)}, 500