from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload

from fastapi import Depends, Response, Body
from fastapi import status
from fastapi.routing import APIRouter

from typing import Annotated, Optional
from annotated_types import Gt

import entities
import dto

from database import sessionmaker

router = APIRouter(
    prefix='/person',
    tags=['Люди']
)


@router.get('', response_model=dto.PersonList)
def get_all():
    query = select(entities.Person)
    with sessionmaker() as session:
        res = session.scalars(query).all()
    return res


@router.get('/{person_id}', response_model=Optional[dto.Person])
def get_one(
        person_id: Optional[Annotated[int, Gt(0)]],
        response: Response
):
    query = select(entities.Person)\
        .where(entities.Person.id == person_id)\
        .options(joinedload(entities.Person.pets))
    with sessionmaker() as session:
        res = session.scalar(query)
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    return res


@router.post('', status_code=status.HTTP_201_CREATED, response_model=dto.Person)
def post_one(person: Annotated[dto.PersonCreate, Body]):
    insert_query = insert(entities.Person).values(**person.model_dump()).returning(entities.Person.id)
    with sessionmaker() as session:
        new_id = session.execute(insert_query).scalar()
        session.commit()
        fetch_query = select(entities.Person)\
            .where(entities.Person.id == new_id)\
            .options(joinedload(entities.Person.pets))
        res = session.scalar(fetch_query)
    return res


@router.put('', response_model=Optional[dto.Person])
def put_one(
        person: Annotated[dto.Person, Body],
        response: Response
):
    fetch_query = select(entities.Person).where(entities.Person.id == person.id)
    update_query = update(entities.Person)\
        .values(person.model_dump(exclude={'id'}))\
        .where(entities.Person.id == person.id)
    join_query = select(entities.Person)\
        .where(entities.Person.id == person.id)\
        .options(joinedload(entities.Person.pets))

    with sessionmaker() as session:
        db_person = session.scalar(fetch_query)
        if db_person is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return

        session.execute(update_query)
        session.commit()

        res = session.scalar(join_query)
    return res


@router.delete('/{person_id}', response_model=Optional[Annotated[int, Gt(0)]])
def delete_one(
        person_id: Annotated[int, Gt(0)],
        response: Response
):
    fetch_query = select(entities.Person)\
        .where(entities.Person.id == person_id)

    delete_query = delete(entities.Person)\
        .where(entities.Person.id == person_id)\
        .returning(entities.Person.id)

    with sessionmaker() as session:
        res = session.scalar(fetch_query)
        if res is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return
        res = session.scalar(delete_query)
        session.commit()
    return res
