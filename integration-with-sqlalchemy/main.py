# Working with Database Metadata

from typing import List, Optional

from sqlalchemy import (Column, ForeignKey, Integer, String, create_engine,
                        inspect, select)
from sqlalchemy.orm import (DeclarativeBase, Mapped, Session, declarative_base,
                            mapped_column, relationship)


# Establishing a declarative base
class Base(DeclarativeBase):
    pass


# Declaring mapped classes
class User(Base):
    __tablename__ = "user_account"

    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    # Relationship
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User({self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"

    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column("user_account.id")

    # Relationship
    user: Mapped["User"] = relationship(back_populates="addresses")

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
