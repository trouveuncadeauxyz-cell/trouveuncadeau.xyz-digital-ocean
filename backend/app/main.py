"""FastAPI Application for TrouveUnCadeau.xyz

Moteur de recommandation de cadeaux intelligents pour Québec
Utilise LangChain pour l'intégration IA et Airtable pour la base de données produits.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from typing import List, Dict, Any
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

# Initialiser FastAPI
app = FastAPI(
    title="TrouveUnCadeau API",
    description="Moteur de recommandation de cadeaux intelligents pour Québec",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Configuration CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8501",  # Streamlit
    "https://trouveuncadeau.xyz",
    "https://www.trouveuncadeau.xyz"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes de santé
@app.get("/health")
async def health_check():
    """Endpoint de vérification de santé du service"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "TrouveUnCadeau API"
    }

@app.get("/api/health")
async def api_health():
    """Endpoint de vérification de santé détaillé"""
    try:
        # Vérifier les variables d'environnement critiques
        required_envs = [
            'OPENAI_API_KEY',
            'AIRTABLE_API_KEY',
            'AIRTABLE_BASE_ID'
        ]
        
        missing_envs = [env for env in required_envs if not os.getenv(env)]
        
        if missing_envs:
            logger.warning(f"Variables d'environnement manquantes: {missing_envs}")
            return {
                "status": "degraded",
                "timestamp": datetime.now().isoformat(),
                "missing_configs": missing_envs
            }
        
        return {
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "environment": os.getenv('ENVIRONMENT', 'development')
        }
    except Exception as e:
        logger.error(f"Erreur lors de la vérification de santé: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Routes racine
@app.get("/")
async def root():
    """Route racine avec informations de l'API"""
    return {
        "message": "Bienvenue à TrouveUnCadeau API",
        "documentation": "/api/docs",
        "health": "/health"
    }

# Placeholder pour routes futures
@app.post("/api/recommendations")
async def get_recommendations(user_input: Dict[str, Any]):
    """Endpoint pour obtenir des recommandations de cadeaux (À implémenter)"""
    logger.info(f"Requête de recommandations reçue: {user_input}")
    return {
        "status": "in_development",
        "message": "Cet endpoint sera disponible à partir de JOUR 2"
    }

@app.get("/api/products")
async def get_products():
    """Endpoint pour récupérer la liste des produits (À implémenter)"""
    logger.info("Requête des produits reçue")
    return {
        "status": "in_development",
        "message": "Intégration Airtable en cours"
    }

# Gestion des erreurs 404
@app.get("/404")
async def not_found():
    raise HTTPException(status_code=404, detail="Route non trouvée")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv('PORT', 8000)),
        reload=os.getenv('ENVIRONMENT', 'development') == 'development'
    )
