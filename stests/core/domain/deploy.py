import typing
from dataclasses import dataclass

from stests.core.domain.enums import DeployStatus
from stests.core.domain.enums import DeployType
from stests.core.utils.domain import *



@dataclass
class Deploy(Entity):
    """Encapsulates information pertaining to a deploy dispatched to a test network.
    
    """
    # Associated block hash in event of finalization. 
    block_hash: str

    # Deploy's payload signature hash (blake). 
    deploy_hash: str

    # Associated network.
    network: str

    # Associated node index.
    node: int

    # Numerical index to distinguish between multiple runs of the same generator.
    run: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str    

    # Deploy's processing status.
    status: DeployStatus

    # Moment in time when deploy dispatched to CLX network.
    ts_dispatched: typing.Optional[int]

    # Moment in time when deploy was finalized by CLX network.
    ts_finalized: typing.Optional[int]

    # Deploy's processing status.
    typeof: DeployType

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()

    # Timestamp: update.
    _ts_updated: typing.Optional[datetime] = None

    # Universally unique identifier.
    _uid: str = get_uuid_field() 
