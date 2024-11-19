from fastapi import APIRouter, Body, Depends, Response, status, Query

from integration_bus.application import dto
from integration_bus.adapters.http_api.dependencies import get_eis_service
from integration_bus.application.services import EisService

from typing import Annotated
from annotated_types import Gt

router = APIRouter(
    prefix='/eis',
    tags=['Внешние информационные системы']
)


@router.get(path='', response_model=dto.eis.RespList)
async def get_eis_list(
        eis_service: Annotated[EisService, Depends(get_eis_service)]
):
    return await eis_service.get_eis_list()


@router.get(path='/{eis_id}', response_model=dto.eis.RespDetail)
async def get_one_eis(
        eis_service: Annotated[EisService, Depends(get_eis_service)],
        eis_id: Annotated[int, Gt(0)],
        response: Response
):
    res = await eis_service.get_eis_by_id(eis_id)

    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response

    response.body = res
    return res


@router.post(path='', response_model=dto.eis.RespDetail, status_code=status.HTTP_201_CREATED)
async def add_eis(
        eis_service: Annotated[EisService, Depends(get_eis_service)],
        eis: dto.eis.ReqCreate = Body()
):
    return await eis_service.add_eis(eis)


@router.put(path='', response_model=dto.eis.RespDetail)
async def update_eis(
        eis_service: Annotated[EisService, Depends(get_eis_service)],
        eis: dto.eis.ReqUpdate = Body()
):
    return await eis_service.update_eis(eis)


@router.delete(path='')
async def delete_eis(
        eis_service: Annotated[EisService, Depends(get_eis_service)],
        response: Response,
        id_: Annotated[int, Gt(0)] = Query()
):
    res = await eis_service.delete_eis(id_)
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    response.status_code = status.HTTP_200_OK
    return response
