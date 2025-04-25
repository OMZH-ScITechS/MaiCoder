from fastapi import APIRouter, Request
import os
import json
import re

router = APIRouter()

submit_dir = "/app/data/submissions/"

@router.get("/{subpath:path}")
async def get_submissions(subpath: str):
    try:
        # Validate subpath format
        if re.fullmatch(r"\d{5}/\d{5}", subpath):  # Format: 5 digits/5 digits
            with open(f"{submit_dir}{subpath}.json", "r") as file:
                content = json.load(file)
            return content
        elif re.fullmatch(r"\d{5}", subpath):  # Format: 5 digits only
            directory_path = os.path.join(submit_dir, subpath)
            if not os.path.isdir(directory_path):
                return {"error": "Directory not found"}, 404
            all_files = {}
            for filename in os.listdir(directory_path):
                if filename.endswith(".json"):
                    with open(os.path.join(directory_path, filename), "r") as file:
                        all_files[filename] = json.load(file)
            return all_files
        else:
            return {"error": "Invalid path format"}, 400
    except FileNotFoundError:
        return {"error": "File not found"}, 404
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}, 400
    except Exception as e:
        return {"error": str(e)}, 500