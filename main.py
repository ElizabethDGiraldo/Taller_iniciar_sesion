from pathlib import Path
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Formulario")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# 4. Base de datos simulada
STUDENT_DATABASE = {
    "correo": "hola@gmail.com",
    "password": "1234",
    "nombre": "Usuario",
}

# 5. Rutas de la aplicación
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    valid_password = (password == STUDENT_DATABASE["password"])

    if not valid_password:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Contraseña incorrecta.",
            },
            status_code=401,
        )

    # Actualizar datos simulados
    STUDENT_DATABASE["correo"] = email.strip().lower()
    STUDENT_DATABASE["nombre"] = email.split("@")[0].capitalize()

    return RedirectResponse(url="/base", status_code=303)

@app.get("/base", response_class=HTMLResponse)
async def home(request: Request):
   
    return templates.TemplateResponse("bienvenido.html", {"request": request, "student": STUDENT_DATABASE})