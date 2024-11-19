from pydantic import BaseModel, RootModel, Field

from dto import PetList


class Person(BaseModel):
    id: int = Field(ge=1)
    name: str
    gender: bool
    pets: PetList
    age: int


class PersonCreate(BaseModel):
    name: str
    gender: bool
    age: int


class PersonListElement(BaseModel):
    id: int = Field(ge=1)
    name: str
    age: int


class PersonList(RootModel[list[PersonListElement]]):
    root: list[PersonListElement]
