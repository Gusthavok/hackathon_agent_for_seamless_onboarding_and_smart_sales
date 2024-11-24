import logging

from sqlalchemy.orm import Session
from database import engine, Base
from models import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(session: Session) -> None:
    Base.metadata.create_all(bind=engine)
    
def init() -> None:
    with Session(engine) as session:
        init_db(session)

def add_data() -> None:
    with Session(engine) as session:
        def create_user(number):

            # password : totototo
            utilisateur = Users(username=f"toto_{number}")

            return utilisateur
            
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