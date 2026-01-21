from fastapi import FastAPI
from app.routers import users, alumno, root, profesor, directivo

app = FastAPI(debug=True)
app.include_router(users.router)
app.include_router(alumno.router)
#app.include_router(root.router)
app.include_router(profesor.router)
app.include_router(directivo.router)

@app.get("/")
async def root_endpoint():
    return {"message": "Bienvenido a nuestra API"}