from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request, db: Session = Depends(get_db)):
    mock_products = [
        {
            "name": "Purificador Facile C7",
            "category": "Bancada / POU",
            "description": "Retenção bacteriológica Classe A. Elimina 99,9% das bactérias e reduz o cloro.",
            "retention_class": "Classe A (0.5 a 1 micra)",
            "bacteriological_efficiency": "Aprovado 99,9%",
            "flow_rate": "40 L/h",
            "refill_lifespan": "5.000 Litros ou 6 Meses",
            "image": "/static/img/products/facile_1.jpg"
        },
        {
            "name": "Purificador Ultramax",
            "category": "Refrigerado por Compressor",
            "description": "Água gelada com ultrafiltração por membrana UF. Máxima segurança bacteriológica.",
            "retention_class": "Ultrafiltração UF",
            "bacteriological_efficiency": "Aprovado 99,9%",
            "flow_rate": "60 L/h",
            "refill_lifespan": "6.000 Litros ou 6 Meses",
            "image": "/static/img/products/ultramax_1.jpg"
        },
        {
            "name": "Filtro Central ECO 9.3/4\"",
            "category": "Ponto de Entrada (POE)",
            "description": "Instalado no cavalete ou caixa d'água. Protege toda a encanação contra barro e areia.",
            "retention_class": "Classe E (20 a 50 micras)",
            "bacteriological_efficiency": "Retenção de Partículas",
            "flow_rate": "1.200 L/h",
            "refill_lifespan": "6 Meses",
            "image": "/static/img/products/eco_1.jpg"
        }
    ]
    
    return templates.TemplateResponse(
        request=request,
        name="public/index.html",
        context={"products": mock_products}
    )

@router.get("/politica-de-privacidade", response_class=HTMLResponse)
async def privacy_policy_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/privacidade.html"
    )
