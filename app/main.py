from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from app.routers import users, alumno, profesor, directivo, actitud, tarea, expediente, curso, horario

# Desactivamos la ruta 'docs' automática
app = FastAPI(debug=True, docs_url=None)

# Inclusión de routers #Aqui arriba poner los nuevos o por testear, que salen antes.

#testeados
app.include_router(tarea.router)
app.include_router(alumno.router)
app.include_router(users.router)
app.include_router(profesor.router)
app.include_router(actitud.router)
app.include_router(expediente.router)
app.include_router(directivo.router) #TODO fix delete
app.include_router(horario.router)
app.include_router(curso.router)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    response = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Dark Mode",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )
    
    # CSS para Modo Oscuro Real (sin filtros de inversión)
    dark_css = """
    <style>
        /* Fondo general */
        body, .swagger-ui { background-color: #1b1b1b !important; color: #ffffff !important; }
        
        /* Textos e Info */
        .swagger-ui .info .title, .swagger-ui .info p, .swagger-ui .info li, 
        .swagger-ui .opblock-tag, .swagger-ui .opblock-summary-description,
        .swagger-ui .tabli button, .swagger-ui label, .swagger-ui .opblock-description-wrapper p { 
            color: #ffffff !important; 
        }

        /* Cuadros de los endpoints (fondo oscuro para que resalte el color original) */
        .swagger-ui .opblock { background: #252525 !important; border: 1px solid #333 !important; }
        .swagger-ui .opblock-summary-path { color: #ffffff !important; }
        
        /* Inputs y Selects */
        .swagger-ui input, .swagger-ui select, .swagger-ui textarea { 
            background: #333 !important; color: white !important; border: 1px solid #444 !important; 
        }

        /* Arreglo de tablas y modelos */
        .swagger-ui .model-box, .swagger-ui section.models { background: #222 !important; border: 1px solid #333 !important; }
        .swagger-ui table thead tr td, .swagger-ui table thead tr th { color: #aaa !important; border-bottom: 1px solid #444 !important; }
        
        /* Quitar la barra superior blanca */
        .swagger-ui .topbar { display: none; }
    </style>
    """
    
    content = response.body.decode().replace("</body>", f"{dark_css}</body>")
    return HTMLResponse(content=content)

@app.get("/")
async def root_endpoint():
    return {"message": "Bienvenido a nuestra API"}