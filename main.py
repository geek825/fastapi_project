

from fastapi import FastAPI, Request, Form , Depends , HTTPException 
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from schema import UserCreate, Userlogin , Expense
from auth import create_access_token , verify_password , hash_password , get_current_user
import psycopg2
from typing import List
import os

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

def get_connection():
    return psycopg2.connect(
        dbname=os.environ.get("expenses_db_041z"),
        user=os.environ.get("expenses_db_041z_user"),
        password=os.environ.get("rjWxMFHHMYBZvCdIQvPJ6mQuWAKb5Z2T"),
        host=os.environ.get("dpg-d2dfujc9c44c73f6n6o0-a"),
        port=os.environ.get("5432")
    )



@app.get("/signup", response_model = UserCreate)
def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup", tags=["signup"])
def signup(user : UserCreate):
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        first_name = user.first_name 
        last_name = user.last_name
        email = user.email
        password = user.password 
        hobbies = user.hobbies 
        
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
@app.get("/login", response_model = Userlogin )
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
@app.post("/login", tags=["login"])
def login(user : Userlogin):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        email = user.email
        password = user.password
    
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
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.post("/expense" , tags= ["expense"])
def add_expense(user : Expense) :
    try :
        conn = get_connection()
        cur = conn.cursor()
        
        amount = user.amount
        description = user.description
        category = user.category
        date = user.date
        
        
        cur = conn.cursor()
        cur.execute("INSERT INTO expenses (amount, description, category, date) VALUES (%s, %s, %s, %s)", (amount, description, category, date))
        conn.commit()
        return {"message": "Expense added successfully"}
    
    except Exception as e :
        return {"error" : str(e)}
    
    
@app.get("/expense" , tags = ["expense"])
def get_expense(current_user: dict = Depends(get_current_user)):
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        
        cur.execute("SELECT user_id, amount, description, category, date FROM expenses WHERE user_id = %s", (current_user["id"],))
        expenses = cur.fetchall()
        
        expeses_list = []
        
        for row in expenses :
            expeses_list.append({
                "id" : row[0] , 
                "amount" : row[1],
                "description" : row[2],
                "category" : row[3],
                "date" : row[4]
            })
            
            return expeses_list
    
   
    except Exception as e:
        return {"error": str(e)}
    finally:
        cur.close()
        conn.close()
            

@app.put("/expense/{id}", tags=["expenses Update"])
def update_expense(id: int , expense : Expense):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM expenses WHERE id = %s ", (id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Expense not found or unauthorized")
        cur.execute("""
            UPDATE expenses 
             SET amount=%s, category=%s, description=%s, date=%s 
            WHERE id=%s
        """, (expense.amount, expense.category, expense.description, expense.date, id ))


        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Expense updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.delete("/expense/{id}" , tags = ["expense delete"])
def delete_expense(id : int) :
    try :
        conn = get_connection()
        
        cur = conn.cursor()
        cur.execute("DELETE FROM expenses WHERE id = %s" , (id,))
        
        if not cur.rowcount:
            conn.rollback()
            raise HTTPException(status_code= 404 , detail = "Expense not")
        
        conn.commit()
        
        return {"message" : "Expenses deleted successfully" }

    except Exception as e :
        return {"error" : str(e)}
    
    
    finally :
        cur.close()
        conn.close()
             