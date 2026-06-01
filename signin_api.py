from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os 
import mysql.connector
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bitlx.onrender.com"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class signin_request(BaseModel):
    email : str
    password : str

@app.get("/")
def working():
    return{"message" : "your api is working"}

@app.post("/signin")
def signin(request : signin_request):
    email = request.email
    password = request.password

    db = None
    cursor = None
    
    try:
        db = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_DATABASE"),
            port=int(os.environ.get("DB_PORT"))
            )

        cursor = db.cursor()
        
        cursor.execute("""
            SELECT * FROM users
            WHERE email = %s and pass = %s
        """,(email, password))

        exist = cursor.fetchone()

        if exist:
            return{"message":"user exist"}
        else:
            return{"message":"user dont exist"}
    
    except mysql.connector.Error as err:
        return {"message": "Database connection failed", "error": str(err)}
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
        
        
            
