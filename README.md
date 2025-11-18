# 🎁 TrouveUnCadeau.xyz

**Moteur de recommandation de cadeaux intelligents pour Québec**

Plate-forme IA alimentée par FastAPI, Streamlit, LangChain et Airtable pour générer des recommandations de cadeaux personnalisées basées sur le budget, l'âge, l'occasion et les intérêts.

---

## 🚀 Fonctionnalités

✨ **Intelligence Artificielle**
- Intégration LangChain avec support multi-modèles (OpenAI GPT-4, Anthropic Claude, Google Gemini)
- Prompts optimisés pour la recommandation de cadeaux en français
- Contexte produit intelligent injecté en temps réel

🎯 **Moteur de Recommandation**
- Filtrage par budget (CAD)
- Recommandations basées sur l'âge du destinataire
- Personnalisation par occasion (anniversaire, Noël, fête, etc.)
- Prise en compte des intérêts spécifiques

📦 **Gestion des Produits**
- Base de données Airtable synchronisée
- 100+ produits avec détails complets
- Liens affiliés Amazon Associates
- Catégorisation intelligente

🌐 **Architecture Scalable**
- Backend FastAPI hautes performances
- Frontend Streamlit responsive
- Déploiement cloud-ready (AWS/Heroku)
- API REST documentée (Swagger)

---

## 📋 Structure du Projet

```
trouveuncadeau/
├── backend/
│   └── app/
│       ├── core/
│       │   └── config.py          # Configuration Pydantic
│       ├── services/
│       │   ├── airtable_service.py    # Intégration Airtable
│       │   └── recommendation_engine.py # Moteur LangChain
│       └── main.py                # Endpoints FastAPI
├── frontend/
│   ├── __init__.py                # Package initialization
│   └── app.py                     # Interface Streamlit
├── .env.example                   # Variables d'environnement
├── requirements.txt               # Dépendances Python
├── README.md                      # Cette documentation
└── .gitignore                     # Fichiers à ignorer
```

---

## 🛠️ Installation

### Prérequis
- Python 3.9+
- pip ou poetry
- Compte Airtable avec base créée
- Clés API pour les modèles IA

### Setup Local

```bash
# Cloner le repository
git clone https://github.com/trouveuncadeauxyz-cell/trouveuncadeau.git
cd trouveuncadeau

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\\Scripts\\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API
```

---

## ▶️ Démarrage

### Backend (FastAPI)

```bash
cd backend
python -m app.main
```

Le serveur sera disponible sur `http://localhost:8000`
API Swagger: `http://localhost:8000/api/docs`

### Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

L'interface sera disponible sur `http://localhost:8501`

---

## 🔑 Configuration

Copier `.env.example` vers `.env` et configurer:

```env
# Airtable
AIRTABLE_API_KEY=your_api_key
AIRTABLE_BASE_ID=appw9JQ4PA66Tryh5
AIRTABLE_TABLE_ID=tblgO4MsNTLEhgJHo

# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Google
GOOGLE_API_KEY=...

# Amazon Associates
AMAZON_ASSOCIATE_TAG=trouveuncadeau-20
```

---

## 📚 Endpoints API

### Santé du Service

```
GET /health
GET /api/health
```

### Produits

```
GET /api/products?limit=100&category=electronics
```

Réponse:
```json
{
  "status": "success",
  "count": 5,
  "products": [
    {
      "id": "rec...",
      "name": "Produit",
      "price": "49.99",
      "category": "electronics",
      "description": "..."
    }
  ]
}
```

### Recommandations

```
POST /api/recommendations
```

Parametres:
- `budget` (float): Budget maximal en CAD (défaut: 50.0)
- `recipient_age` (int): Âge du destinataire (défaut: 25)
- `occasion` (str): Type d'occasion (défaut: "anniversaire")
- `interests` (str): Intérêts du destinataire (défaut: "")
- `count` (int): Nombre de recommandations (défaut: 5)

Réponse:
```json
{
  "status": "success",
  "count": 5,
  "recommendations": [
    {
      "name": "Produit recommandé",
      "price": "45.99",
      "description": "...",
      "category": "...",
      "affiliate_url": "https://amazon.ca/..."
    }
  ]
}
```

---

## 🧠 Moteur IA

### Architecture

- **LangChain** pour orchestration
- **Modèles supportés**: OpenAI GPT-4, Anthropic Claude, Google Gemini
- **Prompt System**: MEGA_META_PROMPT optimisé pour recommandations cadeaux
- **Context Injection**: Produits injectés dynamiquement dans le contexte

### Exemple de Flux

1. Utilisateur fournit préférences via Streamlit
2. Récupération des produits dans le budget via Airtable
3. Injection des produits dans le contexte LangChain
4. Générations de recommandations via modèle IA
5. Formatage et retour au frontend

---

## 📊 Données Airtable

Structure de la table "Products":
- **Name**: Nom du produit
- **Price**: Prix en CAD
- **Category**: Catégorie (electronics, fashion, gifts, etc.)
- **Description**: Description détaillée
- **URL**: Lien vers le produit
- **AmazonURL**: Lien affilié Amazon
- **Tags**: Tags pour recherche

---

## 🚢 Déploiement Production

### AWS

```bash
eb init trouveuncadeau
eb create production
eb deploy
```

### Heroku

```bash
heroku create trouveuncadeau
git push heroku main
```

### Docker

```bash
docker build -t trouveuncadeau .
docker run -p 8000:8000 trouveuncadeau
```

---

## 📅 Timeline (JOUR 1-13)

- ✅ **JOUR 1 (Nov 18)**: Infrastructure & foundation (9 fichiers)
- ✅ **JOUR 2 (Nov 18-19)**: Services & API integration (3 fichiers)
- 🔄 **JOUR 3-7 (Nov 19-23)**: Optimisation backend & features
- 🔄 **JOUR 8-9 (Nov 24-25)**: Production deployment
- 🔄 **JOUR 10-12 (Nov 26-28)**: Testing & marketing
- ⏰ **JOUR 13 (Nov 29-30)**: LAUNCH & PREMIÈRE VENTE ⏰

---

## 📝 Logs & Monitoring

```bash
# Voir les logs du backend
tail -f backend/app.log

# Vérifier l'état des services
curl http://localhost:8000/api/health
```

---

## 🤝 Contribution

Pour contribuer:

1. Fork le repository
2. Créer une branche (`git checkout -b feature/amazing`)
3. Commit les changements (`git commit -am 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing`)
5. Ouvrir une Pull Request

---

## 📄 Licence

MIT License - voir LICENSE.md pour détails

---

## 👥 Auteurs

- **TrouveUnCadeau Team** - Plate-forme IA pour recommandation de cadeaux au Québec

---

## 📞 Support

Pour questions ou support:
- Email: support@trouveuncadeau.xyz
- Issues: GitHub Issues
- Documentation: https://trouveuncadeau.xyz/docs

---

**Deadline CRITIQUE: PREMIÈRE VENTE AVANT MINUIT - November 30, 2025 🎯**
