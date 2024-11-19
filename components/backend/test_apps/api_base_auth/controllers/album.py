from fastapi import Depends, Response, Body
from fastapi import status
from fastapi.routing import APIRouter
from fastapi.security import HTTPBasicCredentials

import entities
import dto
from mock_data import ALBUMS
from auth import basic_auth, check_credentials

from typing import Annotated, Optional
from annotated_types import Gt

from random import uniform

router = APIRouter(
    prefix='/album',
    tags=['Альбомы']
)


@router.get('', response_model=Optional[dto.AlbumList])
def get_all(
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    return ALBUMS


@router.get('/{album_id}', response_model=Optional[dto.Album])
def get_one(
        album_id: Optional[Annotated[int, Gt(0)]],
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    for a in ALBUMS:
        if a.id == album_id:
            return a
    response.status_code = status.HTTP_404_NOT_FOUND


@router.post('', response_model=Optional[dto.Album])
def post_one(
        album: Annotated[dto.AlbumCreate, Body],
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    return entities.Album(**album.model_dump(), id=int(uniform(1, 100)), compositions=[], rating=0)


@router.put('', response_model=Optional[dto.Album])
def put_one(
        album: Annotated[dto.Album, Body],
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    found = False
    for a in ALBUMS:
        if a.id == id:
            found = True
            break

    if not found:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    return entities.Album(**album.model_dump())


@router.delete('/{album_id}', response_model=Optional[Annotated[int, Gt(0)]])
def delete_one(
        album_id: Annotated[int, Gt(0)],
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    for a in ALBUMS:
        if a.id == album_id:
            return a.id
    response.status_code = status.HTTP_404_NOT_FOUND
