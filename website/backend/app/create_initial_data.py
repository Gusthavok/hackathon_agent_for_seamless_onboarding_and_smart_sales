import logging

from sqlalchemy.orm import Session
from database import engine, Base
from models import *

import json 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(session: Session) -> None:
    Base.metadata.create_all(bind=engine)
    
def init() -> None:
    with Session(engine) as session:
        init_db(session)

def load_products(file_path: str, session: Session):
    # Initialiser un compteur de produits et un lot de produits à ajouter
    batch_size = 100  # Taille du lot de produits à insérer en une seule fois
    batch = []

    with open(file_path, "r") as file:
        for line in file:
            # Convertir chaque ligne en un dictionnaire Python
            data = json.loads(line)

            # Vérifier si l'un des champs importants est None
            if data.get("price") == "None":
                data["price"] = None
            if (
                data.get("price") is None or
                data.get("main_category") is None or
                data.get("title") is None or
                data.get("average_rating") is None or
                data.get("rating_number") is None or
                data.get("features") is None or
                data.get("description") is None or
                data.get("images") is None or
                data.get("videos") is None or
                data.get("store") is None or
                data.get("categories") is None or
                data.get("details") is None or
                data.get("parent_asin") is None or
                data.get("price") == "" or
                data.get("main_category") == "" or
                data.get("title") == "" or
                data.get("average_rating") == "" or
                data.get("rating_number") == "" or
                data.get("features") == "" or
                data.get("description") == "" or
                data.get("images") == "" or
                data.get("videos") == "" or
                data.get("store") == "" or
                data.get("categories") == "" or
                data.get("details") == "" or
                data.get("parent_asin") == ""
            ):
        # Votre code pour gérer l'erreur ou la condition ici

                continue  # Si un champ est None, passer à l'itération suivante
            images=dict(data["images"])
            images = [{
                        "hi_res": images["hi_res"][0],
                        "thumb":  images["thumb"][0],
                        "large":  images["large"][0],
                        "variant":  images["variant"][0]
                    }]
            videos=dict(data["videos"])
            videos = []
            details=data["details"]

            # Créer une instance de ProductModel si tous les champs sont valides
            print('########', data["price"])
            produit = ProductModel(
                main_category=data["main_category"],
                title=data["title"],
                average_rating=data["average_rating"],
                rating_number=data["rating_number"],
                features=data["features"],
                description=data["description"],
                price=data["price"],
                images=images,
                videos=videos,
                store=data["store"],
                categories=data["categories"],
                details=details,
                parent_asin=data["parent_asin"],
                bought_together=data.get("bought_together", None)  # Cela peut être None sans problème
            )

            # Ajouter l'instance à la liste (batch)
            batch.append(produit)

            # Si la taille du lot atteint le batch_size, ajouter tous les produits à la session
            if len(batch) >= batch_size:
                session.add_all(batch)  # Ajout de tous les produits dans le batch
                session.commit()  # Effectuer le commit pour enregistrer les données
                batch.clear()  # Réinitialiser le lot de produits

        # Ajouter les restes des produits restants
        if batch:
            session.add_all(batch)
            session.commit()
            

def add_data() -> None:
    with Session(engine) as session:
        def create_user(number):

            # password : totototo
            utilisateur = Users(username=f"toto_{number}")

            return utilisateur
        
        load_products("./utils/final_running_products", session)
                
        users_list = []
        for k in range(7):
            usr = create_user(k)
            users_list.append(usr)
            session.add(usr)

        session.commit()
        


def main() -> None:
    logger.info("Creating tables")
    init()
    logger.info("Inserting values")
    add_data()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()