from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    health_measurement = Column(String, index=True)
    value = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("patients.id"))

    owner = relationship("Patient", back_populates="measurements")