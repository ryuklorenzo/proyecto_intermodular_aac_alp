from fastapi import FastAPI
from app.routers import users

app = FastAPI(debug=True)
app.include_router(users.router)

@app.get("/")
async def root():
    return{"Bienvenido a nuestra API "}