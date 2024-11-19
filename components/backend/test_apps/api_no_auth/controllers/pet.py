from sqlalchemy import select, insert, update, delete

from fastapi import Response, Body
from fastapi import status
from fastapi.routing import APIRouter

from typing import Annotated, Optional
from annotated_types import Gt

import entities
import dto

from database import sessionmaker

router = APIRouter(
    prefix='/pet',
    tags=['Питомцы']
)


@router.get('', response_model=dto.PetList)
def get_all():
    query = select(entities.Pet)
    with sessionmaker() as session:
        res = session.scalars(query).all()
    return res


@router.get('/{pet_id}', response_model=Optional[dto.Pet])
def get_one(
        pet_id: Optional[Annotated[int, Gt(0)]],
        response: Response
):
    query = select(entities.Pet).where(entities.Pet.id == pet_id)
    with sessionmaker() as session:
        res = session.scalar(query)
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    return res


@router.post('', status_code=status.HTTP_201_CREATED, response_model=dto.Pet)
def post_one(pet: Annotated[dto.PetCreate, Body]):
    insert_query = insert(entities.Pet).values(**pet.model_dump()).returning(entities.Pet.id)
    with sessionmaker() as session:
        new_id = session.scalar(insert_query)
        session.commit()
        fetch_query = select(entities.Pet).where(entities.Pet.id == new_id)
        res = session.scalar(fetch_query)
    return res


@router.put('', response_model=Optional[dto.Pet])
def put_one(
        pet: Annotated[dto.Pet, Body],
        response: Response
):
    fetch_query = select(entities.Pet).where(entities.Pet.id == pet.id)
    update_query = update(entities.Pet)\
        .values(pet.model_dump(exclude={'id'}))\
        .where(entities.Pet.id == pet.id)

    with sessionmaker() as session:
        db_pet = session.scalar(fetch_query)
        if db_pet is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return

        session.execute(update_query)
        session.commit()
        session.refresh(db_pet)
    return db_pet


@router.delete('/{pet_id}', response_model=Optional[Annotated[int, Gt(0)]])
def delete_one(
        pet_id: Annotated[int, Gt(0)],
        response: Response
):
    fetch_query = select(entities.Pet) \
        .where(entities.Pet.id == pet_id)

    delete_query = delete(entities.Pet)\
        .where(entities.Pet.id == pet_id)\
        .returning(entities.Pet.id)

    with sessionmaker() as session:
        res = session.scalar(fetch_query)
        if res is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return
        res = session.scalar(delete_query)
        session.commit()
    return res
