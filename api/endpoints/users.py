from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import os
import mysql.connector
from hashlib import sha256
import jwt
from datetime import datetime, timedelta

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")

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
            "INSERT INTO users (name, pass) VALUES (%s, %s)",
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
            "SELECT * FROM users WHERE name = %s AND pass = %s",
            (name, hashed_password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            return JSONResponse(content={"error": "Invalid username or password"}, status_code=401)

        # Generate JWT token
        payload = {
            "sub": user["name"],
            "exp": datetime.utcnow() + timedelta(days=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return JSONResponse(content={"access_token": token, "token_type": "bearer"}, status_code=200)
    except mysql.connector.Error as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)