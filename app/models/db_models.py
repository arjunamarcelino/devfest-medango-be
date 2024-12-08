from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

# User Model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, nullable=False)
    created_at = Column(String, default="NOW()")

    itineraries = relationship('Itinerary', back_populates='user')

# Itinerary Model
class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    activity_type = Column(String, nullable=False)
    created_at = Column(String, default="NOW()")

    user = relationship("User", back_populates="itineraries")
    activities = relationship("Activity", back_populates="itinerary")

# Activity Model
class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)
    day = Column(Integer, nullable=False)
    time = Column(String, nullable=False)
    location = Column(String, nullable=False)
    full_address = Column(Text, nullable=False)
    activity_type = Column(String, nullable=False)
    notes = Column(Text, nullable=True)

    itinerary = relationship("Itinerary", back_populates="activities")
