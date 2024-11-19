"""Insert data

Revision ID: 503af0d29c7b
Revises: d85460e17e6d
Create Date: 2023-08-28 18:12:44.898877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table


# revision identifiers, used by Alembic.
revision: str = '503af0d29c7b'
down_revision: Union[str, None] = 'd85460e17e6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


person_table = table(
    'person',
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('gender', sa.Boolean(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
)

pet_table = table(
    'pet',
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('gender', sa.Boolean(), nullable=False),
    sa.Column('animal', sa.String(length=128), nullable=False),
    sa.Column('owner_id', sa.ForeignKey('person.id'), nullable=False),
)

persons = [
    {'name': 'John', 'gender': True, 'age': 30},
    {'name': 'Emily', 'gender': False, 'age': 25},
    {'name': 'Michael', 'gender': True, 'age': 35},
    {'name': 'Sophia', 'gender': False, 'age': 28},
    {'name': 'William', 'gender': True, 'age': 32}
]

pets = [
    {'name': 'Max', 'age': 3, 'gender': True, 'animal': 'dog', 'owner_id': 1},
    {'name': 'Bella', 'age': 2, 'gender': False, 'animal': 'cat', 'owner_id': 2},
    {'name': 'Charlie', 'age': 4, 'gender': True, 'animal': 'dog', 'owner_id': 3},
    {'name': 'Lucy', 'age': 1, 'gender': False, 'animal': 'dog', 'owner_id': 2},
    {'name': 'Rocky', 'age': 5, 'gender': True, 'animal': 'cat', 'owner_id': 4}
]


def upgrade() -> None:
    op.bulk_insert(person_table, persons)
    op.bulk_insert(pet_table, pets)


def downgrade() -> None:
    pet_ids = tuple(pet['id'] for pet in pets)
    op.execute(f'DELETE FROM pet WHERE pet.id IN {pet_ids}')
    person_ids = tuple(person['id'] for person in persons)
    op.execute(f'DELETE FROM person WHERE person.id IN {person_ids}')
