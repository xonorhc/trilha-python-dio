from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"

    # atributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    fullname = Column(String)

    # relationship
    address = relationship("Address", back_populates="user", cascade="all")

    def __repr__(self):
        return f"User({self.id=}: {self.name=}, {self.fullname=})"


class Address(Base):
    __tablename__ = "user_address"

    # atributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_address = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    # relationship
    user = relationship("User", back_populates="address")

    def __repr__(self) -> str:
        return f"Address({self.id=}: {self.email_address=})"
