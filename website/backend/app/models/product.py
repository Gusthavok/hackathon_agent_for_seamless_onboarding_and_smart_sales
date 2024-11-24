from sqlalchemy import Column, String, Float, Integer, JSON
from database import Base

class ProductModel(Base):
    __tablename__ = "products"
    
    id = Column(Float, primary_key=True, index=True)
    main_category = Column(String, nullable=False)
    title = Column(String, nullable=False)
    average_rating = Column(Float, nullable=False)
    rating_number = Column(Float, nullable=False)
    features = Column(JSON, nullable=False)  # Stocke une liste de chaînes
    description = Column(JSON, nullable=False)  # Stocke une liste de chaînes
    price = Column(Float, nullable=False)
    images = Column(JSON, nullable=False)  # Stocke une liste d'objets Image
    videos = Column(JSON, nullable=False)  # Stocke une liste d'objets Video
    store = Column(String, nullable=False)
    categories = Column(JSON, nullable=False)  # Stocke une liste de chaînes
    details = Column(JSON, nullable=False)  # Stocke un dictionnaire
    parent_asin = Column(String, nullable=False)
    bought_together = Column(JSON, nullable=True)  # Stocke une liste ou null


