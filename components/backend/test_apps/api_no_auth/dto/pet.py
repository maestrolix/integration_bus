from pydantic import RootModel, BaseModel


class Pet(BaseModel):
    id: int
    name: str
    age: int
    gender: bool
    animal: str
    owner_id: int


class PetCreate(BaseModel):
    name: str
    age: int
    gender: bool
    animal: str
    owner_id: int


class PetListElement(BaseModel):
    id: int
    name: str
    animal: str


class PetList(RootModel[list[PetListElement]]):
    root: list[PetListElement]
