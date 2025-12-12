from fastapi import FastAPI
from app.routers import users, alumno, root

app = FastAPI(debug=True)
app.include_router(users.router)
app.include_router(alumno.router)
app.include_router(root.router)

@app.get("/")
async def root():
    return{"Bienvenido a nuestra API "}