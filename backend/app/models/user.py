from sqlalchemy import Column, Integer, String, Enum
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(
        Enum("candidate", "company", "admin", name="user_role"), default="candidate"
    )
