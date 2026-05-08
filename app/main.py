from fastapi import FastAPI
from app.routers import users, alumno, profesor, directivo, actitud, tarea, expediente

app = FastAPI(debug=True)
app.include_router(users.router)
app.include_router(alumno.router)
app.include_router(profesor.router)
app.include_router(directivo.router)
app.include_router(actitud.router)
app.include_router(tarea.router)
app.include_router(expediente.router)

@app.get("/")
async def root_endpoint():
    return {"message": "Bienvenido a nuestra API"}