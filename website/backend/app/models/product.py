from sqlalchemy import Column, String, Float, Integer, JSON, ARRAY 
from database import Base

class ProductModel(Base):
    __tablename__ = "products"
    
    id = Column(Float, primary_key=True, index=True)
    main_category = Column(String, nullable=True)
    title = Column(String, nullable=True)
    average_rating = Column(Float, nullable=True)
    rating_number = Column(Float, nullable=True)
    features = Column(JSON, nullable=True)  # Stocke une liste de chaînes
    description = Column(JSON, nullable=True)  # Stocke une liste de chaînes
    price = Column(Float, nullable=True)
    images = Column(JSON, nullable=True)  # Stocke une liste d'objets Image
    videos = Column(JSON, nullable=True)  # Stocke une liste d'objets Video
    store = Column(String, nullable=True)
    categories = Column(JSON, nullable=True)  # Stocke une liste de chaînes
    details = Column(JSON, nullable=True)  # Stocke un dictionnaire
    parent_asin = Column(String, nullable=True)
    bought_together = Column(JSON, nullable=True)  # Stocke une liste ou null

