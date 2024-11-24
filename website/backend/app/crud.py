from models.users import Users
from sqlalchemy.orm import sessionmaker, Session

def create_user(username:str, name: str, email: str, phone: str) -> bool:

    try:
        # Exemple : simulation d'une insertion dans une base de données
        print(f"Saving data: Name = {name}, Email = {email}, Phone = {phone}")
        
        # Retourner True si l'enregistrement est réussi
        return True
    except Exception as e:
        print(f"Error while saving user data: {e}")
        return False

def user_exist(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first() is not None


