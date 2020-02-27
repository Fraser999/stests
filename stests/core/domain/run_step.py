import typing
from dataclasses import dataclass
from datetime import datetime

from stests.core.domain.enums import RunStepStatus
from stests.core.utils.domain import *



@dataclass
class RunStep(Entity):
    """Step information associated with a generator run.
    
    """
    # Associated network.
    network: str

    # Numerical index to distinguish between multiple runs of the same generator.
    run: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str

    # Current status.
    status: RunStepStatus

    # Step name.
    step: str

    # Moment in time when step occurred.
    ts_start: datetime

    # Moment in time when step completed.
    ts_end: typing.Optional[datetime]

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()

    # Timestamp: update.
    _ts_updated: typing.Optional[datetime] = None

    # Universally unique identifier.
    _uid: str = get_uuid_field() 

    @property
    def name(self):
        return self.step

    @property
    def phase(self):
        return self.step.split(".")[0]

    @property
    def action(self):
        return self.step.split(".")[-1]
