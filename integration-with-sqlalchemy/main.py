# Working with Database Metadata

from sqlalchemy import (Column, ForeignKey, Integer, String, create_engine,
                        inspect, select)
from sqlalchemy.orm import Session, declarative_base, relationship

# Establishing a declarative base
Base = declarative_base()

# TODO: Convert an old-style Declarative class to the new style,
# Using ORM declarative forms to define table metadata


# Declaring mapped classes
class User(Base):
    __tablename__ = "user_account"

    # Attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    fullname = Column(String)

    # Relationship
    address = relationship("Address", back_populates="user", cascade="all")

    def __repr__(self):
        return f"User({self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"

    # Attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_address = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    # Relationship
    user = relationship("User", back_populates="address")

    def __repr__(self) -> str:
        return f"Address({self.id!r}, email_address={self.email_address!r})"


# Establishing connectivity
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# Create all tables stored in this metadata.
Base.metadata.create_all(engine)

# Performs database schema inspection.
insp = inspect(engine)
print(insp.get_table_names())

# Create session and add objects
with Session(engine) as session:
    mary = User(
        name="mary",
        fullname="Mary Jane",
        address=[Address(email_address="jane_mary@mail.com")],
    )

    john = User(
        name="john",
        fullname="John Jones",
        address=[
            Address(email_address="jones_john@mail.com"),
            Address(email_address="jjones@mail.com"),
        ],
    )

    peter = User(name="peter", fullname="Peter Park")

    # Framing out a BEGIN / COMMIT / ROLLBACK block
    session.begin()
    try:
        session.add_all([mary, john, peter])
    except Exception as e:
        session.rollback()
        raise e
    else:
        session.commit()

# Querying
with Session(engine) as session:
    # Query for ``User`` objects
    statement = select(User).filter_by(name="Mary")

    # List of ``User`` objects
    user_obj = session.scalars(statement).all()

    # Query for individual columns
    statement = select(User.name, User.fullname)

    # List of Row objects
    rows = session.execute(statement).all()
