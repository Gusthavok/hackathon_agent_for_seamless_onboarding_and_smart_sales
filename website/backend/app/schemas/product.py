
from typing import Optional, List, Dict
from pydantic import BaseModel


class Image(BaseModel):
    hi_res: str
    thumb: str
    large: str
    variant: str 

class Video(BaseModel):
    title: str
    url: str    

class Product(BaseModel):
    main_category: str
    title: str
    average_rating: float
    rating_number: float
    features: List[str]
    description: List[str]
    price: float
    images: List[Image]
    videos: List[Video]
    store: str
    categories: List[str]
    parent_asin: str
    bought_together: Optional[List[str]]
