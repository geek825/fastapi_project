
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from schema import UserCreate, Userlogin
from auth import create_access_token , verify_password , hash_password
import psycopg2
from typing import List
import os

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))
@app.get("/signup", response_class=HTMLResponse)
def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup", tags=["signup"])
def signup(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    hobbies: List[str] = Form(...)
):
    try:
        conn = psycopg2.connect(
            dbname="daily",
            user="postgres",
            password="12345",
            host="localhost",
            port="5433"
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return {"message": "User already exists"}

        hashed_pwd = hash_password(password)
        cur.execute(
            "INSERT INTO users (first_name, last_name, email, password, hobbies) VALUES (%s, %s, %s, %s, %s)",
            (first_name, last_name, email, hashed_pwd, hobbies)
        )
        conn.commit()
        return {"message": "User signup successful"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            cur.close()
            conn.close()
@app.get("/login", response_class=HTMLResponse)
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
@app.post("/login", tags=["login"])
def login(email: str = Form(...), password: str = Form(...)):
    try:
        conn = psycopg2.connect(
            dbname="daily",
            user="postgres",
            password="12345",
            host="localhost",
            port="5433"
        )
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        result = cur.fetchone()
        if not result:
            return {"message": "User not found"}

        user_id, stored_password = result
        if not verify_password(password, stored_password):
            return {"message": "Invalid password"}

        access_token = create_access_token(data={"sub": str(user_id)})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            cur.close()
            conn.close()
