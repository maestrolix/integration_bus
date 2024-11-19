from sqlalchemy.types import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from entities import Base


class Pet(Base):
    __tablename__ = 'pet'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128))
    age: Mapped[int]
    gender: Mapped[bool]
    animal: Mapped[str] = mapped_column(String(128))
    owner_id: Mapped[int] = mapped_column(ForeignKey('person.id', ondelete='CASCADE'))
