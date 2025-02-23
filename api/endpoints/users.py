from fastapi import APIRouter, Request
import os

router = APIRouter()

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
}

@router.post("/register")
async def register_user(request: Request):
    #ユーザー登録とか
    print()

@router.post("/login")
async def login_user(request: Request):
    #ここにログイン時の処理
    print()