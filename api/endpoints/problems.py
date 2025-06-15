from fastapi import APIRouter, Request, HTTPException, Depends, BackgroundTasks
from fastapi.security import HTTPBearer
import os
import json
import jwt
import requests
from datetime import datetime

router = APIRouter()
problems_dir = "/app/data/problems/"
contests_dir = "/app/data/contests/"
submit_dir = "/app/data/submissions/"
SECRET_KEY = os.getenv("SECRET_KEY")
security = HTTPBearer()

def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/{subpath:path}")
async def get_problems(subpath: str):
    try:
        if subpath == "":  # Root path
            all_files = []
            for filename in os.listdir(problems_dir):
                if filename.endswith(".json"):
                    with open(os.path.join(problems_dir, filename), "r") as file:
                        file_content = json.load(file)
                        del file_content["tests"]
                        file_content["id"] = filename[:-5]
                        all_files.append(file_content)
            return all_files
        else:
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

def fetch_active_contests():
    try:
        contests_url = "http://api.maicoder.f5.si/contests/active"  # Replace with the actual endpoint
        response = requests.get(contests_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch active contests: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching active contests: {e}")
        return []

async def run_tests(subpath: str, submit_id: str):
    try:
        submission_file_path = f"{submit_dir}{subpath}/{submit_id}.json"

        # Load the submission file
        with open(submission_file_path, "r") as submission_file:
            submission_data = json.load(submission_file)

        # Load the problem file to get the tests
        problem_file_path = f"{problems_dir}{subpath}.json"
        with open(problem_file_path, "r") as problem_file:
            problem_data = json.load(problem_file)
            tests = problem_data.get("tests", [])

        passed_count = 0
        wrong_count = 0
        error_count = 0

        for i, test in enumerate(tests, start=1):
            try:
                # Prepare Wandbox API payload
                code = submission_data.get("code", 'print("hello world")')
                compiler = submission_data.get("compiler", "pypy-3.7-v7.3.9")
                stdin = test["input"]

                url = "https://wandbox.org/api/compile.json"
                payload = {
                    "code": code,
                    "compiler": compiler,
                    "stdin": stdin
                }

                # Call Wandbox API
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    actual_output = result.get("program_output", "").strip()
                    expected_output = test["output"].strip()

                    # Compare outputs
                    if actual_output == expected_output:
                        passed_count += 1
                    else:
                        wrong_count += 1
                else:
                    error_count += 1
            except Exception:
                error_count += 1

            # Determine the status
            if error_count > 0:
                status = "RE"
            elif wrong_count > 0:
                status = "WA"
            elif passed_count == len(tests):
                status = "AC"
            else:
                status = "IP"

            # Update the submission file incrementally
            total_tests = len(tests)
            submission_data["test_results"] = {
                "passed": passed_count,
                "wrong": wrong_count,
                "error": error_count,
                "total": total_tests,
                "status": status
            }
            with open(submission_file_path, "w") as submission_file:
                json.dump(submission_data, submission_file)

            print(f"Test {i}/{total_tests} processed for submission {submit_id} in {subpath}")

        # If status is AC, fetch active contests and perform actions
        if status == "AC":
            active_contests = fetch_active_contests()
            for contest in active_contests:
                # Example: Check if the problem belongs to the contest and update files
                if subpath in contest.get("problems", []):
                    contest_path = f"{contests_dir}{contest['id']}"
                    result_file_path = f"{contest_path}/result.json"

                    if os.path.exists(result_file_path):
                        with open(result_file_path, "r") as result_file:
                            contest_results = json.load(result_file)

                        # Update contest results (example logic)
                        # Ensure the 'test' key exists in 'score'
                        username = submission_data.get("user", "unknown")
                        if username not in contest_results["score"]:
                            contest_results["score"][username] = {"problems": []}

                        # Append the problem ID, score, and user to the 'problems' list
                        contest_results["score"][username]["problems"].append({
                            subpath: submission_data.get("score", 0)
                        })

                        with open(result_file_path, "w") as result_file:
                            json.dump(contest_results, result_file)

    except Exception as e:
        print(f"Error running tests for submission {submit_id} in {subpath}: {e}")

@router.post("/submit/{subpath:path}")
async def submit_problem(
    subpath: str, 
    request: Request, 
    background_tasks: BackgroundTasks, 
    current_user: str = Depends(get_current_user)
):
    try:
        data = await request.json()

        # Add username to the submission data
        data["user"] = current_user
        data["time"] = datetime.utcnow().isoformat()

        # Load the problem file to get the number of tests
        problem_file_path = f"{problems_dir}{subpath}.json"
        print(f"Attempting to access problem file: {problem_file_path}")  # Debugging log
        if not os.path.exists(problem_file_path):
            print(f"Problem file not found: {problem_file_path}")  # Debugging log
            return {"error": "File not found"}, 404

        with open(problem_file_path, "r") as problem_file:
            problem_data = json.load(problem_file)
            total_tests = len(problem_data.get("tests", []))

        # Add placeholder test results to the submission data
        data["test_results"] = {
            "passed": 0,
            "wrong": 0,
            "error": 0,
            "total": total_tests,
            "status": "WJ"
        }

        os.makedirs(submit_dir + subpath, exist_ok=True)

        existing_files = [f for f in os.listdir(submit_dir + subpath) if f.endswith(".json")]
        submit_id = str(len(existing_files) + 1).zfill(5)
        
        with open(f"{submit_dir}{subpath}/{submit_id}.json", "w") as file:
            json.dump(data, file)

        # Add the test execution to background tasks
        background_tasks.add_task(run_tests, subpath, submit_id)
        
        result = {
            "status": "success",
            "submit_id": submit_id,
            "submitted_by": current_user
        }
        
        return result
    except FileNotFoundError:
        return {"error": "File not found"}, 404
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}, 400
    except Exception as e:
        return {"error": str(e)}, 500

@router.post("/post")
async def post_problem(
    request: Request, 
    current_user: str = Depends(get_current_user)
):
    try:
        data = await request.json()

        # Add username to the problem data
        data["user"] = current_user

        existing_files = [f for f in os.listdir(problems_dir) if f.endswith(".json")]
        problem_id = str(len(existing_files) + 1).zfill(5)
        
        with open(f"{problems_dir}{problem_id}.json", "w") as file:
            json.dump(data, file)
        
        return {"problem_id": problem_id}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}, 400
    except Exception as e:
        return {"error": str(e)}, 500