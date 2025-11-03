# Working with Database Metadata

from sqlalchemy import (Column, ForeignKey, Integer, String, create_engine,
                        inspect)
from sqlalchemy.orm import declarative_base, relationship

# establishing a declarative base
Base = declarative_base()


# using orm declarative forms to define table metadata
class User(Base):
    __tablename__ = "user_account"

    # attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    fullname = Column(String)

    # relationship
    address = relationship("Address", back_populates="user", cascade="all")

    def __repr__(self):
        return f"User({self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


# declaring mapped classes
class Address(Base):
    __tablename__ = "address"

    # attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_address = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    # relationship
    user = relationship("User", back_populates="address")

    def __repr__(self) -> str:
        return f"Address({self.id!r}, email_address={self.email_address!r})"


# establishing connectivity
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# create all tables stored in this metadata.
Base.metadata.create_all(engine)

# performs database schema inspection.
insp = inspect(engine)
print(insp.get_table_names())
