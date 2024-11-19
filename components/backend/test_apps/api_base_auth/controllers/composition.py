from random import uniform

from fastapi import Body, Depends, Response, status
from typing import Annotated, Optional
from annotated_types import Gt
from fastapi.routing import APIRouter
from fastapi.security import HTTPBasicCredentials

import dto
import entities

from mock_data import COMPOSITIONS
from auth import check_credentials, basic_auth


router = APIRouter(
    prefix='/composition',
    tags=['Произведения']
)


@router.get('', response_model=Optional[dto.CompositionList])
def get_all(
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    return COMPOSITIONS


@router.get('/{composition_id}', response_model=Optional[dto.Composition])
def get_one(
        composition_id: Optional[Annotated[int, Gt(0)]],
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    for a in COMPOSITIONS:
        if a.id == composition_id:
            return a
    response.status_code = status.HTTP_404_NOT_FOUND


@router.post('', response_model=Optional[dto.Composition])
def post_one(
        composition: Annotated[dto.CompositionCreate, Body],
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    return entities.Composition(**composition.model_dump(), id=int(uniform(1, 100)), rating=0)


@router.put('', response_model=Optional[dto.Composition])
def put_one(
        composition: Annotated[dto.Composition, Body],
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    found = False
    for a in COMPOSITIONS:
        if a.id == id:
            found = True
            break

    if not found:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    return entities.Composition(**composition.model_dump())


@router.delete('/{composition_id}', response_model=Optional[Annotated[int, Gt(0)]])
def delete_one(
        composition_id: Annotated[int, Gt(0)],
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
        response: Response
):
    if not check_credentials(credentials):
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    for a in COMPOSITIONS:
        if a.id == composition_id:
            return a.id
    response.status_code = status.HTTP_404_NOT_FOUND
