from fastapi import APIRouter, Depends

from integration_bus.application import dto

from typing import Annotated


router = APIRouter(
    prefix='/event',
    tags=['События']
)
