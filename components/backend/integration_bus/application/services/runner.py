from dataclasses import dataclass

from integration_bus.application import entities, interfaces, dto

from typing import Optional, Any


@dataclass
class RunnerService:
    runner_repo: interfaces.IRunnerRepository
    eis_repo: interfaces.IEisRepository

    async def get_runners_list(self) -> list[entities.Runner]:
        return await self.runner_repo.get_runners_list()

    async def get_runner_by_id(self, id_: int) -> Optional[dto.runner.RespDetail]:
        db_runner = await self.runner_repo.get_runner_by_id(id_)
        if db_runner is None:
            return None

        dict_runner = db_runner.__dict__
        dict_runner.pop('_sa_instance_state', None)
        dict_runner['eis_from_name'] = db_runner.eis_from.title
        dict_runner['eis_to_name'] = db_runner.eis_to.title
        dict_runner['available_eis_from'] = await self.eis_repo.get_eis_list_of_kind(db_runner.eis_from_kind)
        dict_runner['available_eis_to'] = await self.eis_repo.get_eis_list_of_kind(db_runner.eis_to_kind)

        deps = []
        for dep in db_runner.dependencies:
            new_dep = dep.__dict__
            new_dep.pop('_sa_instance_state', None)
            deps.append(new_dep)
        dict_runner['dependencies'] = deps

        return dto.runner.RespDetail.model_validate(dict_runner)

    async def update_runner(self, runner: dto.runner.ReqUpdate) -> Optional[entities.Runner]:
        if not await self.runner_repo.check_if_exists_by_id(runner.id):
            return None
        await self.runner_repo.update_runner(runner)
        db_runner = await self.runner_repo.get_runner_by_id(runner.id)
        return db_runner
