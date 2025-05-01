from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import os
import mysql.connector
from hashlib import sha256
import jwt
from datetime import datetime, timedelta

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")

image_dir = "/app/data/users/icons/"

@router.post("/register")
async def register_user(request: Request):
    body = await request.json()
    name = body.get("user")
    password = body.get("pass")

    if not name or not password:
        return JSONResponse(content={"error": "Name and password are required"}, status_code=400)

    hashed_password = sha256(password.encode()).hexdigest()

    try:
        conn = mysql.connector.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host='192.168.0.3',
            database='maicoder'
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (user, pass) VALUES (%s, %s)",
            (name, hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        payload = {
            "sub": name,
            "exp": datetime.utcnow() + timedelta(days=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return JSONResponse(content={"access_token": token, "token_type": "bearer"}, status_code=200)
    except mysql.connector.Error as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/login")
async def login_user(request: Request):
    body = await request.json()
    name = body.get("user")
    password = body.get("pass")

    if not name or not password:
        return JSONResponse(content={"error": "Name and password are required"}, status_code=400)

    # Hash the password
    hashed_password = sha256(password.encode()).hexdigest()

    try:
        conn = mysql.connector.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host='192.168.0.3',
            database='maicoder'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE user = %s AND pass = %s",
            (name, hashed_password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            return JSONResponse(content={"error": "Invalid username or password"}, status_code=401)

        # Generate JWT token
        payload = {
            "sub": name,
            "exp": datetime.utcnow() + timedelta(days=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return JSONResponse(content={"access_token": token, "token_type": "bearer"}, status_code=200)
    except mysql.connector.Error as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@router.put("/{user}/icon")
async def upload_icon(user: str, request: Request):
    try:
        form = await request.form()
        file = form.get("image")

        if not file:
            return JSONResponse(content={"error": "No file provided"}, status_code=400)

        filename = f"{user}.png"
        file_path = os.path.join(image_dir, filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        return JSONResponse(content={"message": "Icon uploaded successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/{user}/icon")
async def get_icon(user: str):
    try:
        file_path = os.path.join(image_dir, f"{user}.png")
        if not os.path.exists(file_path):
            file_path = os.path.join(image_dir, "default.png")

        with open(file_path, "rb") as f:
            content = f.read()

        return JSONResponse(content=content, media_type="image/png", status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)