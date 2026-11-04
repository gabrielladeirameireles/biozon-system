from app.database import SessionLocal, engine, Base
from app.models.product import Product

Base.metadata.create_all(bind=engine)
db = SessionLocal()

products_data = [
    # --- LINHA POU (PONTO DE USO) ---
    {
        "name": "Purificador Ultramax (Água Gelada)",
        "category": "POU - Gelada",
        "description": "Purificador de água gelada por compressor de alta eficiência. Conta com ultrafiltração por membrana UF (retém vírus e bactérias até 0,001µm) e opção de mineralização alcalina.",
        "retention_class": "Classe A (0,5 a 1 micra)",
        "bacteriological_efficiency": "Aprovado INMETRO (Dupla Proteção)",
        "chlorine_reduction": "Aprovado (≥ 75%)",
        "flow_rate": "50 L/h",
        "refill_lifespan": "5.000 Litros ou 6 meses",
        "image_url": "/static/uploads/ultramax.jpg"
    },
    {
        "name": "Purificador Facile C7 (Bacteriológico)",
        "category": "POU - Bancada/Parede",
        "description": "Purificador compacto de conexão rápida. Elimina 99,9% das bactérias da água, reduz o cloro e retém sedimentos como barro, limo e areia.",
        "retention_class": "Classe A",
        "bacteriological_efficiency": "Aprovado (99,9% eliminação)",
        "chlorine_reduction": "Aprovado (≥ 75%)",
        "flow_rate": "40 L/h",
        "refill_lifespan": "3.000 Litros ou 6 meses",
        "image_url": "/static/uploads/facile-c7.jpg"
    },
    {
        "name": "Purificador MultiFacile C3 / C7 (Sob a Pia)",
        "category": "POU - Sob a Pia",
        "description": "Solução oculta para instalação embaixo de pias, torneiras gourmet, máquinas de café e suco. Mantém a bancada livre.",
        "retention_class": "Classe A/C",
        "bacteriological_efficiency": "Aprovado (opção Refil C7)",
        "chlorine_reduction": "Aprovado (≥ 75%)",
        "flow_rate": "40 L/h",
        "refill_lifespan": "10.000 Litros ou 6 meses",
        "image_url": "/static/uploads/multifacile.jpg"
    },
    
    # --- LINHA POE (PONTO DE ENTRADA / CAIXA D'ÁGUA) ---
    {
        "name": "Filtro Hidrofiltros ECO 9.3/4\"",
        "category": "POE - Entrada/Cavalete",
        "description": "Instalado no cavalete ou antes da caixa d'água. Evita o acúmulo de sujeira, barro e areia em toda a rede hidráulica da casa.",
        "retention_class": "Classe D (25 micras)",
        "bacteriological_efficiency": "Não aplicável (Retenção de Partículas)",
        "chlorine_reduction": "Não aplicável",
        "flow_rate": "1.200 L/h",
        "refill_lifespan": "Aproximadamente 6 meses (Refil Lavável Polyflow)",
        "image_url": "/static/uploads/filtro-eco.jpg"
    },
    {
        "name": "Filtro BIG 10\" / BIG 20\"",
        "category": "POE - Altas Vazões / Condomínios",
        "description": "Filtro de alta capacidade para entradas de condomínios, empresas e residências de grande porte. Alta resistência e alta vazão.",
        "retention_class": "Classe C/D",
        "bacteriological_efficiency": "Não aplicável",
        "chlorine_reduction": "Não aplicável",
        "flow_rate": "4.200 L/h a 6.000 L/h",
        "refill_lifespan": "6 meses",
        "image_url": "/static/uploads/filtro-big.jpg"
    },

    # --- REFIS DE REPOSIÇÃO MULTIUSO ---
    {
        "name": "Refil Multiuso HF-ELX (Compatível Electrolux)",
        "category": "Refil Multiuso",
        "description": "Compatível com modelos Electrolux PE11, PC41, PH41, PA21, PE12, entre outros. Redução de cloro e gosto desagradável.",
        "retention_class": "Classe C",
        "bacteriological_efficiency": "Bacteriostático",
        "chlorine_reduction": "Aprovado (≥ 75%)",
        "flow_rate": "50 a 60 L/h",
        "refill_lifespan": "5.000 Litros ou 6 meses",
        "image_url": "/static/uploads/refil-electrolux.jpg"
    },
    {
        "name": "Refil Multiuso HF+3 / HF+7 (Compatível IBBL)",
        "category": "Refil Multiuso",
        "description": "Compatível com purificadores IBBL FR600, Evolux, Atlantis, Mio e Viváx. Tripla ou septupla filtragem com ação bacteriostática.",
        "retention_class": "Classe C",
        "bacteriological_efficiency": "Aprovado",
        "chlorine_reduction": "Aprovado (≥ 75%)",
        "flow_rate": "40 a 60 L/h",
        "refill_lifespan": "3.000 a 4.000 Litros ou 6 meses",
        "image_url": "/static/uploads/refil-ibbl.jpg"
    }
]

for item in products_data:
    existing = db.query(Product).filter(Product.name == item["name"]).first()
    if not existing:
        prod = Product(**item)
        db.add(prod)

db.commit()
db.close()
print("Produtos do catálogo Hidrofiltros inseridos com sucesso!")

