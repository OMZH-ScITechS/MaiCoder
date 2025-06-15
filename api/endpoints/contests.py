from fastapi import APIRouter, Request
import os
import json
from datetime import datetime

router = APIRouter()
contests_dir = "/app/data/contests/"

@router.get("/{subpath:path}")
async def get_contest_datail(subpath: str):
    try:
        if subpath == "":  # Root path
            all_files = []
            for contest_name in os.listdir(contests_dir):
                contest_path = os.path.join(contests_dir, contest_name, "about.json")
                if os.path.isfile(contest_path):
                    with open(contest_path, "r") as file:
                        file_content = json.load(file)
                        del file_content["problems"]
                        all_files.append(file_content)
            return all_files
        elif subpath == "active":
            all_files = []
            for contest_name in os.listdir(contests_dir):
                contest_path = os.path.join(contests_dir, contest_name, "about.json")
                if os.path.isfile(contest_path):
                    with open(contest_path, "r") as file:
                        content = json.load(file)
                        contest_date = datetime.fromisoformat(content.get("date"))
                        if contest_date < datetime.now():
                            all_files.append(content)
            return all_files
        else:
            with open(f"{contests_dir}{subpath}/about.json", "r") as file:
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

        # Correctly access the 'name' field from the JSON data
        contest_id = data["name"].lower()
        contest_path = f"{contests_dir}{contest_id}"

        # Ensure the directory exists
        os.makedirs(contest_path, exist_ok=True)

        with open(f"{contest_path}/about.json", "w") as file:
            json.dump(data, file)
        with open(f"{contest_path}/result.json", "w") as result_file:
            json.dump({"score": []}, result_file)
        return {"contest_id": contest_id}
    except KeyError:
        return {"error": "'name' field is required in the JSON data"}, 400
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}, 400
    except Exception as e:
        return {"error": str(e)}, 500