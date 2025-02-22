from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"]
)

# Import the routers from the new files
from endpoints import judge, problems, contests

# Include the routers
app.include_router(judge.router, prefix="/judge")
app.include_router(problems.router, prefix="/problems")
app.include_router(contests.router, prefix="/contests")