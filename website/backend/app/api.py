from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import Base, engine, SessionLocal
from random import random
from typing import List
from schemas.product import Product  # Le modèle Pydantic pour sérialiser la réponse
import uvicorn


import crud

db = SessionLocal()

# Initialisation de l'application
app = FastAPI()

# Middleware pour gérer les CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplacez '*' par les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modèle pour les données d'entrée
class ChatbotRequest(BaseModel):
    conversation: list[dict]
    username: str
    cart: dict

class ConnexionRequest(BaseModel):
    username: str

# Exemple de route
@app.get("/")
async def root():
    return {"message": "Backend fonctionne !"}

# Route pour le chatbot
@app.post("/chatbot")
async def chatbot_endpoint(request: ChatbotRequest):
    conversation = request.conversation
    if not conversation:
        raise HTTPException(status_code=400, detail="Conversation vide.")
    
    reply, new_url = crud.get_answer_bot(db, conversation, request.username, request.cart)
    
    return {"reply": reply, 
            "redirect": new_url}

# Route pour vérifier la connexion d'un utilisateur
@app.post("/api/connexion")
async def connexion_endpoint(request: ConnexionRequest):
    username = request.username
    # Vérifier si l'utilisateur existe
    exists = crud.user_exist(db, username)
    return {"exists": exists}

@app.get("/api/products", response_model=List[Product])
async def products_endpoint(request: Request):
    username = request.headers.get("Username")
    # try:
    print("patato")
    products = crud.get_products(db, username)  # Récupère les produits depuis la BDD
    return products  # FastAPI convertit automatiquement les objets en JSON
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des produits: {e}")


class UserData(BaseModel):
    username: str
    name: str
    email: str
    phone: str

@app.post("/api/createUser")
async def create_user_endpoint(user_data: UserData):
    # Appel de la fonction pour enregistrer les données dans la base de données
    result = crud.create_user(user_data.username, user_data.name, user_data.email, user_data.phone)
    if result:
        return {"message": "Données enregistrées avec succès."}
    else:
        raise HTTPException(status_code=500, detail="Erreur lors de l'enregistrement des données.")


# Exécuter l'application (si vous utilisez un serveur comme Uvicorn)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
