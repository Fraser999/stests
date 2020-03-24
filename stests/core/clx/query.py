import typing
from datetime import datetime

from stests.core.clx import utils
from stests.core.domain import Account
from stests.core.domain import Block
from stests.core.domain import BlockStatus
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.utils import factory

from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import MessageToJson


@utils.clx_op
def get_balance(ctx: ExecutionContext, account: Account) -> int:
    """Returns a chain account balance.

    :param ctx: Execution context information.
    :param account: Account whose balance will be queried.

    :returns: Account balance.

    """
    _, client = utils.get_client(ctx)
    try:
        balance = client.balance(
            address=account.public_key,
            block_hash=get_last_block_hash(client)
            )
    except Exception as err:
        if "Failed to find base key at path" in err.details:
            return 0
        raise err
    else:
        return balance


@utils.clx_op
def get_block_by_node(
    node_id: NodeIdentifier,
    block_hash: str
    ) -> typing.Union[typing.Dict, Block]:
    """Queries network for information pertaining to a specific block.

    :param node_id: A node identifier.
    :param block_hash: Hash of a block.

    :returns: 2 member tuple: (block info, block summary).

    """
    _, client = utils.get_client(node_id)
    block_info = client.showBlock(block_hash_base16=block_hash, full_view=False)

    return MessageToDict(block_info), factory.create_block(
        network_id=node_id.network,
        block_hash=block_hash,
        deploy_cost_total=block_info.status.stats.deploy_cost_total,
        deploy_count=block_info.summary.header.deploy_count, 
        deploy_gas_price_avg=block_info.status.stats.deploy_gas_price_avg,
        j_rank=block_info.summary.header.j_rank,
        m_rank=block_info.summary.header.main_rank,
        size_bytes=block_info.status.stats.block_size_bytes,
        timestamp=datetime.fromtimestamp(block_info.summary.header.timestamp / 1000.0),
        validator_id=block_info.summary.header.validator_public_key.hex()
        )


@utils.clx_op
def get_deploys_by_node(node_id: NodeIdentifier, block_hash: str) -> typing.List[typing.Union[str, typing.Dict]]:
    """Queries node for a set of deploys associated with a specific block.

    :param node_id: A node identifier.
    :param block_hash: Hash of a block.

    :returns: 2 member tuple: (deploy hash, deploy info).

    """
    _, client = utils.get_client(node_id)
    deploys = client.showDeploys(block_hash_base16=block_hash, full_view=False)

    return ((i.deploy.deploy_hash.hex(), MessageToDict(i)) for i in deploys)


@utils.clx_op
def get_last_block_hash(client) -> str:
    """Returns a chain's last block hash.
    
    """
    last_block_info = next(client.showBlocks(1))

    return last_block_info.summary.block_hash.hex()


@utils.clx_op
def get_contract_hash(ctx: ExecutionContext, account: Account, dhash: str) -> str:
    """Returns hash of an on-chain contract.
    
    :param ctx: Execution context information.
    :param account: On-chain account under which contract was deployed.
    :param dhash: Hash of a previously processed deploy.

    :returns: Hash of on-chain contract.

    """
    _, client = utils.get_client(ctx)

    dinfo = client.showDeploy(dhash, wait_for_processed=True)
    bhash = dinfo.processing_results[0].block_info.summary.block_hash.hex()
    chash = utils.get_contract_hash(client, account, bhash, "counter")

    return chash