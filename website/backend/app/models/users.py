from datetime import datetime
from database import Base
from sqlalchemy import ForeignKey, Column, String, Float,  DateTime, Text, func
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
    historique_coversations_precedentes = Column(Text, nullable=False, default= '')