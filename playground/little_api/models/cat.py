from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from db.base_class import Base


class Cat(Base):
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Float, nullable=False)
    color = Column(String(100), nullable=False)
    description = Column(String(1000), index=True, nullable=True)
    name = Column(String(100), nullable=False)
    status = Column(String(100), nullable=False)
    caretaker_id = Column(String(10), ForeignKey("user.id"), nullable=True)
    caretaker = relationship("User", back_populates="cats") #cats is created in user model
