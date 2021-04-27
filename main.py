"""
Run the live server with command: uvicorn main:app --reload
"""

# --- Static Files ---
# You can serve static files automatically from a directory using StaticFiles.
# Install aiofiles -> pip install aiofiles
# Install jinja2 -> pip install jinja2


from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.exception_handler(StarletteHTTPException)  # Página ERROR 404
async def custom_http_exception_handler(request, exc):
    return templates.TemplateResponse("404.html", {"request": request})


@app.get("/metodologia", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("metodologia.html", {"request": request})


@app.get("/prevision", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("prevision.html", {"request": request})


@app.get("/comercio", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("comercio.html", {"request": request})


@app.get("/frutas", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas.html", {"request": request})


@app.get("/naranja", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/naranja_page.html", {"request": request})


@app.get("/pera", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/pera_page.html", {"request": request})


@app.get("/manzana", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/manzana_page.html", {"request": request})


@app.get("/platano", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/platano_page.html", {"request": request})


@app.get("/fresa", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/fresa_page.html", {"request": request})


@app.get("/albaricoque", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/albaricoque_page.html", {"request": request})


@app.get("/kiwi", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/kiwi_page.html", {"request": request})


@app.get("/melocoton", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/melocoton_page.html", {"request": request})


@app.get("/pina", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/pina_page.html", {"request": request})


@app.get("/sandia", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/sandia_page.html", {"request": request})


@app.get("/melon", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/melon_page.html", {"request": request})


@app.get("/aguacate", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/aguacate_page.html", {"request": request})


@app.get("/limon", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/limon_page.html", {"request": request})


@app.get("/verduras", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("verduras.html", {"request": request})


@app.get("/tomate", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("verduras/tomate_page.html", {"request": request})


@app.get("/ajo", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("verduras/ajo_page.html", {"request": request})


@app.get("/cebolla", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("verduras/cebolla_page.html", {"request": request})


@app.get("/lechuga", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("verduras/lechuga_page.html", {"request": request})


@app.get("/zanahoria", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("verduras/zanahoria_page.html", {"request": request})


@app.get("/alcachofa", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("verduras/alcachofa_page.html", {"request": request})


@app.get("/calabacin", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("verduras/calabacin_page.html", {"request": request})


@app.get("/berenjena", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("verduras/berenjena_page.html", {"request": request})


@app.get("/esparrago", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("verduras/esparrago_page.html", {"request": request})


@app.get("/pepino", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/pepino_page.html", {"request": request})


@app.get("/pimiento", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("frutas/pimiento_page.html", {"request": request})


@app.get("/patata", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("verduras/patata_page.html", {"request": request})


@app.get("/conclusiones", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("conclusiones.html", {"request": request})


@app.get("/referencias", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("referencias.html", {"request": request})


# Endpoint creado para verificar que el servidor esta en marcha
@app.get("/ping")
async def ping():
    return {"result": "pong"}
