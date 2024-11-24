from datetime import datetime
from database import Base
from sqlalchemy import ForeignKey, Column, String, Float,  DateTime, Text, func, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    appetance_prix = Column(Float, nullable=False, default='.5')
    appetance_discount = Column(Float, nullable=False, default='.5')
    sprint = Column(Float, nullable=False, default='.2')
    fond = Column(Float, nullable=False, default='.2')
    demifond = Column(Float, nullable=False, default='.2')
    ultratrail = Column(Float, nullable=False, default='.2')
    genre = Column(Float, nullable=False, default='.5')
    age = Column(Float, nullable=False, default='30.')
    sante = Column(Float, nullable=False, default='.9')
    product_for_user=Column(JSON, nullable=False, default=[ "B07FNFJ8CH", "B0BLRX62NJ", "B07GKCMXY3", "B07Q58J93Q", "B01G1ETJR8", "B09HZH6Q1M"])
    historique_coversations_precedentes = Column(Text, nullable=False, default= '')
