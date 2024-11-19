from integration_bus.application import services


class Services:
    eis: services.EisService
    runner: services.RunnerService
    router: services.RouterService
    dependency_validation_service: services.DependencyValidationService


def get_eis_service():
    return Services.eis


def get_runner_service():
    return Services.runner


def get_router_service():
    return Services.router


def get_dependency_validation_service(): 
    return Services.dependency_validation_service