from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.root import router as roots_router

app = FastAPI(debug=True)

app.include_router(users_router)
app.include_router(roots_router)

@app.get("/")
async def root_endpoint():
    return {"message": "Bienvenido a nuestra API"}