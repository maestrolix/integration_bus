from pydantic import BaseModel, RootModel, Field
from datetime import datetime


class Composition(BaseModel):
    id: int
    title: str
    rating: float = Field(ge=0, le=5)


class CompositionCreate(BaseModel):
    title: str


class CompositionList(RootModel[list[Composition]]):
    root: list[Composition]


class AlbumCreate(BaseModel):
    title: str
    release_date: datetime


class Album(BaseModel):
    id: int
    title: str
    release_date: datetime
    compositions: CompositionList
    rating: float = Field(ge=0, le=5)


class AlbumListElement(BaseModel):
    id: int
    title: str
    release_date: datetime
    rating: float = Field(ge=0, le=5)


class AlbumList(RootModel[list[AlbumListElement]]):
    root: list[AlbumListElement]


class Artist(BaseModel):
    id: int
    name: str
    albums: AlbumList
    rating: float = Field(ge=0, le=5)


class ArtistCreate(BaseModel):
    name: str


class ArtistListElement(BaseModel):
    id: int
    name: str
    rating: float = Field(ge=0, le=5)


class ArtistList(RootModel[list[ArtistListElement]]):
    root: list[ArtistListElement]
