from sqlalchemy.types import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from entities import Base


class Person(Base):
    __tablename__ = 'person'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    gender: Mapped[bool]
    pets: Mapped[list["Pet"]] = relationship(backref='owner', cascade='all, delete-orphan')
    age: Mapped[int]
