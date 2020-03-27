import dataclasses
import typing
from datetime import datetime

from stests.core.domain.block import Block
from stests.core.domain.enums import DeployStatus
from stests.core.domain.enums import DeployType



@dataclasses.dataclass
class Deploy:
    """Encapsulates information pertaining to a deploy dispatched to a test network.
    
    """
    # Index of account with which the deploy is associated.
    account_index: typing.Optional[int]

    # Associated block hash in event of finalization. 
    block_hash: typing.Optional[str]

    # Associated block rank. 
    block_rank: typing.Optional[int]

    # Deploy's payload signature hash (blake). 
    deploy_hash: str

    # Node to which deploy was dispatched.
    dispatch_node: int

    # Moment in time when deploy dispatched to CLX network.
    dispatch_ts: typing.Optional[datetime]

    # Node which emitted finalization event of the block in which deploy was included.
    finalization_node: typing.Optional[int]

    # Time between dispatch & deploy finality.
    finalization_time: typing.Optional[float]

    # Flag indicating whether time to finalization was acceptable.
    finalization_time_is_acceptable: typing.Optional[bool]

    # Tolerance of time between dispatch & deploy finality.
    finalization_time_tolerance: typing.Optional[float]
    
    # Moment in time when deploy was finalized by CLX network.
    finalization_ts: typing.Optional[datetime]

    # Associated network.
    network: str

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: int

    # Type of generator, e.g. WG-100 ...etc.
    run_type: str    

    # Deploy's processing status.
    status: DeployStatus

    # Deploy's processing status.
    typeof: DeployType

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    @property
    def hash(self):
        return self.deploy_hash

    @property
    def is_from_run(self):
        return self.run_type is not None

    @property
    def label_finalization_time(self):
        if self.finalization_time:
            return format(self.finalization_time, '.4f')
        return "--"

    @property
    def label_account_index(self):
        return f"A-{str(self.account_index).zfill(6)}"

    @property
    def label_run_index(self):
        return f"R-{str(self.run_index).zfill(3)}"


    def update_on_finalization(self, block: Block):
        """Executed when deploy has been finalized.
        
        """
        self.block_hash = block.hash
        self.block_rank = block.m_rank
        self.status = DeployStatus.FINALIZED
        self.finalization_ts = block.timestamp
        self.finalization_time = block.timestamp.timestamp() - self.dispatch_ts.timestamp()
