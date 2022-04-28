from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from db.base_class import Base


# note: index=True for WHERE filter fields
class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    email = Column(String, index=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    cats = relationship(
        "Cat",
        cascade="all,delete-orphan",
        back_populates="caretaker",
        uselist=True,
    )