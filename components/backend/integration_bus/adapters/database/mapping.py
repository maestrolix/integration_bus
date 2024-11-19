from sqlalchemy.orm import backref, registry, relationship

from integration_bus.adapters.database import tables
from integration_bus.application import entities

mapper = registry()

mapper.map_imperatively(
    entities.Eis,
    tables.eis
)

mapper.map_imperatively(
    entities.Runner,
    tables.runners,
    properties={
        'eis_from': relationship(
            entities.Eis,
            foreign_keys=[tables.runners.c.eis_from_id],
            lazy='select'
        ),
        'eis_to': relationship(
            entities.Eis,
            foreign_keys=[tables.runners.c.eis_to_id],
            lazy='select'
        ),
        'mock_dataset': relationship(
            entities.MockData,
            collection_class=list,
            back_populates='runner'
        ),
        'dependencies': relationship(
            entities.Runner,
            secondary=tables.runners_dependencies,
            primaryjoin=tables.runners_dependencies.c.runner_id == tables.runners.c.id,
            secondaryjoin=tables.runners_dependencies.c.dependency_runner_id == tables.runners.c.id,
            backref=backref('dependants', lazy='select', join_depth=1),
            lazy='select',
            join_depth=1
        )
    }
)

mapper.map_imperatively(
    entities.RunnerDependency,
    tables.runners_dependencies
)

mapper.map_imperatively(
    entities.MockData,
    tables.mock_data,
    properties={
        'runner': relationship(
            entities.Runner,
            foreign_keys=[tables.mock_data.c.runner_id],
            back_populates='mock_dataset'
        )
    }
)


mapper.map_imperatively(
    entities.RunnerExecutionRequest,
    tables.runner_execution_requests,
)

mapper.map_imperatively(
    entities.RunnerEvent, 
    tables.runner_events,
    properties={
        'runner': relationship(
            entities.Runner,
            foreign_keys=[tables.runner_events.c.runner_id]
        )
    }
)

mapper.map_imperatively(
    entities.RunnerLog, 
    tables.runner_logs
)