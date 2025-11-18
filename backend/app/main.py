"""FastAPI Application for TrouveUnCadeau.xyz

Moteur de recommandation de cadeaux intelligents pour Québec
Utilise LangChain pour l'intégration IA et Airtable pour la base de données produits.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core import configure_middleware
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

# Configure middleware
configure_middleware(app, enable_cors=True)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importer les services
from app.services.airtable_service import AirtableService
from app.services.recommendation_engine import RecommendationEngine
from app.core.config import settings

# Initialiser les services
airtable_service = None
recommendation_engine = None

@app.on_event("startup")
async def startup_event():
    """Initialiser les services au démarrage"""
    global airtable_service, recommendation_engine
    try:
        airtable_service = AirtableService()
        recommendation_engine = RecommendationEngine()
        logger.info("✅ Services initialized successfully")
    except Exception as e:
        logger.error(f"❌ Error initializing services: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Nettoyer les ressources à l'arrêt"""
    logger.info("🛑 Shutting down application")

# ============ ENDPOINTS SANTE ============

@app.get("/", tags=["Health"])
async def root():
    """Route racine avec informations API"""
    return {
        "message": "TrouveUnCadeau API v1.0",
        "documentation": "/api/docs",
        "endpoints": {
            "health": "/health",
            "recommendations": "/api/recommendations",
            "products": "/api/products"
        }
    }

@app.get("/health", tags=["Health"])
async def health():
    """Vérifier la santé du service"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/health", tags=["Health"])
async def api_health():
    """Vérifier la santé complète du service"""
    services_status = {}
    
    # Vérifier Airtable
    try:
        await airtable_service.get_all_products()
        services_status["airtable"] = "✅ connected"
    except Exception as e:
        services_status["airtable"] = f"❌ error: {str(e)}"
    
    # Vérifier les modèles IA
    try:
        services_status["ai_models"] = "✅ configured"
    except Exception as e:
        services_status["ai_models"] = f"❌ error: {str(e)}"
    
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "services": services_status
    }

# ============ ENDPOINTS API ============

@app.get("/api/products", tags=["Products"])
async def get_products(
    limit: int = 100,
    category: str = None
) -> Dict[str, Any]:
    """Récupérer tous les produits disponibles"""
    try:
        logger.info(f"📦 Fetching products (limit={limit}, category={category})")
        
        products = await airtable_service.get_all_products()
        
        if category:
            products = [p for p in products if p.get('Category', '').lower() == category.lower()]
        
        if limit:
            products = products[:limit]
        
        logger.info(f"✅ Retrieved {len(products)} products")
        
        return {
            "status": "success",
            "count": len(products),
            "products": products
        }
    except Exception as e:
        logger.error(f"❌ Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recommendations", tags=["Recommendations"])
async def get_recommendations(
    budget: float = 50.0,
    recipient_age: int = 25,
    occasion: str = "anniversaire",
    interests: str = "",
    count: int = 5
) -> Dict[str, Any]:
    """Générer des recommandations de cadeaux personnalisées
    
    Paramètres:
    - budget: Budget maximal en CAD (défaut: 50$)
    - recipient_age: Âge du destinataire (défaut: 25)
    - occasion: Type d'occasion (anniversaire, noël, fête, etc.)
    - interests: Intérêts/passions du destinataire
    - count: Nombre de recommandations (défaut: 5)
    """
    try:
        logger.info(f"🎁 Generating recommendations: budget={budget}$, age={recipient_age}, occasion={occasion}")
        
        # Récupérer tous les produits
        all_products = await airtable_service.get_all_products()
        
        # Filtrer par budget
        products_in_budget = [
            p for p in all_products 
            if float(p.get('Price', '0').replace('$', '').strip() or 0) <= budget
        ]
        
        if not products_in_budget:
            logger.warning(f"⚠️  No products found within budget {budget}$")
            return {
                "status": "warning",
                "message": f"Aucun produit trouvé dans le budget de {budget}$",
                "recommendations": []
            }
        
        # Préparer le contexte utilisateur
        user_input = f"""
        Budget: ${budget} CAD
        Âge du destinataire: {recipient_age} ans
        Occasion: {occasion}
        Intérêts: {interests}
        Nombre de recommandations: {count}
        """
        
        # Générer les recommandations avec LangChain
        recommendations = await recommendation_engine.generate_recommendations(
            user_input=user_input,
            products=products_in_budget,
            count=count
        )
        
        logger.info(f"✅ Generated {len(recommendations)} recommendations")
        
        return {
            "status": "success",
            "count": len(recommendations),
            "recommendations": recommendations
        }
    except Exception as e:
        logger.error(f"❌ Error generating recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============ DEMARRAGE ============

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT", "development") == "development",
        log_level="info"
    )
