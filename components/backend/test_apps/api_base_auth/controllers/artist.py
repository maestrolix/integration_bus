from random import uniform

from fastapi import Body, Depends, Response, status
from typing import Annotated, Optional
from annotated_types import Gt
from fastapi.routing import APIRouter
from fastapi.security import HTTPBasicCredentials

import dto
import entities

from mock_data import ARTISTS
from auth import check_credentials, basic_auth


router = APIRouter(
    prefix='/artist',
    tags=['Исполнители']
)


@router.get('', response_model=Optional[dto.ArtistList])
def get_all(
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    return ARTISTS


@router.get('/{artist_id}', response_model=Optional[dto.Artist])
def get_one(
        artist_id: Optional[Annotated[int, Gt(0)]],
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    for a in ARTISTS:
        if a.id == artist_id:
            return a
    response.status_code = status.HTTP_404_NOT_FOUND


@router.post('', response_model=Optional[dto.Artist])
def post_one(
        artist: Annotated[dto.ArtistCreate, Body],
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    return entities.Artist(**artist.model_dump(), id=int(uniform(1, 100)), albums=[], rating=0)


@router.put('', response_model=Optional[dto.Artist])
def put_one(
        artist: Annotated[dto.Artist, Body],
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    found = False
    for a in ARTISTS:
        if a.id == id:
            found = True
            break

    if not found:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    return entities.Album(**artist.model_dump())


@router.delete('/{artist_id}', response_model=Optional[Annotated[int, Gt(0)]])
def delete_one(
        artist_id: Annotated[int, Gt(0)],
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    for a in ARTISTS:
        if a.id == artist_id:
            return a.id
    response.status_code = status.HTTP_404_NOT_FOUND

