from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import Base, engine, SessionLocal
from random import random

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
    
    last_message = conversation[-1].get("text", "")
    reply = f"Vous avez dit : \"{last_message}\". Voici ma réponse."
    new_url = '/cart' if random()>.5 else '/'
    return {"reply": reply, 
            "redirect": new_url}

# Route pour vérifier la connexion d'un utilisateur
@app.post("/api/connexion")
async def connexion_endpoint(request: ConnexionRequest):
    username = request.username
    # Vérifier si l'utilisateur existe
    exists = crud.user_exist(db, username)
    return {"exists": exists}

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
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
