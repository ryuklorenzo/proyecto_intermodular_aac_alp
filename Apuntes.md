# Archivo Requeriments
- Uvicorn es el servicio que nos permite escribir middleware en python
- Pydantic nos permite crear dataclases, controla los tipos de datos
- Tambien existe guvicorn pero no se uso porque no maneja multitarea

# En la estructura del proyecto
En la raiz tenemos:

- Carpeta **_app_** con los archivos .py
- Carpeta **_db_** con las cosas de bases de datos
- Carpeta **_Docker_** con los dockefiles

# Archivo init.py
El uso de tener un archivo llamado __ init.py __ hace que la carpeta donde esta sea un modulo importable para otras clases.

# Uso de comando uvicorn


--
$ uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
--

En nuestro ejemplo haremos el uso de uvicorn, seguido de el directorio y el archivo donde esta la app (app.main), seguido de dos puntos y el nombre de la app (app). Añadimos el puerto de escucha y en localhost con (0.0.0.0)

# FAST API
Importando los modulos "**_FASTAPI_**" y "_**status**_"
ejemplo decorador:

--
@app.post("/users/singup", status_code = status.HTTP_201_CREATED)
--

# Clase UserIn(BaseModel):

Meter dentro los datos del json que tenemos que recibir en nuestra peticion. ejemplo: 

- username : str
- pwd : str
- name : str

# Como organizar las tablas de get post delete etc.
Dentro del directorio app creamos una carpeta llamada routers
Dentro de esta carpeta crearemos archivos .py segun las tablas que creemos. ejemplo

--
usuarios.py, profesores.py, horario.py
--

dentro de cada una de estas clases hay que crear lo siguiente:
```
router = APIRouter (
	prefix = "/users",
	tags = ["Users]
)

class UserDb(BaseModel):
	id: str
	name: str
	username: str
	password: str

class UserIn(BaseModel):
	username: str
	password: str
	name: str

users: list[UserDb] = []

@router.post("/signup/", status_code.HTTP_201_CREATED)
async def create_user(userIn:UserIn):
	usersFound = [u for u in users if u.username == userIn.username]
	id len(usersFound) < 0:
		raise HTTPException(
			status_code = status.HTTP_409_CONFLICT,
			detail="Username already exists"
)

users.append(
	newUser = UserDb(
		id =, 
		name=In.name,
		username=userIn.username,
		password=userIn.password
	)
)
```

