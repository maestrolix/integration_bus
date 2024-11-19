from fastapi import APIRouter, Body, Depends, Response, status

from integration_bus.application import dto
from integration_bus.adapters.http_api.dependencies import get_runner_service, get_router_service
from integration_bus.application.services import RunnerService, RouterService

from typing import Annotated
from annotated_types import Gt

router = APIRouter(
    prefix='/runner',
    tags=['Раннеры']
)


@router.get(path='', response_model=dto.runner.RespList)
async def get_runners_list(
        runner_service: Annotated[RunnerService, Depends(get_runner_service)]
):
    return await runner_service.get_runners_list()


@router.get(path='/{runner_id}', response_model=dto.runner.RespDetail)
async def get_one_runner(
        runner_service: Annotated[RunnerService, Depends(get_runner_service)],
        runner_id: Annotated[int, Gt(0)],
        response: Response
):
    res = await runner_service.get_runner_by_id(runner_id)
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    return res


@router.post('/{runner_key}')
async def execute_runner(
        router_service: Annotated[RouterService, Depends(get_router_service)],
        runner_key: str
):
    await router_service.route(runner_key)


@router.put(path='', response_model=dto.runner.RespDetail)
async def update_runner(
        runner_service: Annotated[RunnerService, Depends(get_runner_service)],
        runner: dto.runner.ReqUpdate = Body()
):
    return await runner_service.update_runner(runner)
