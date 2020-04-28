import random
import typing

from stests.core import factory
from stests.core.cache.model import CacheItem
from stests.core.cache.model import CacheItemKey
from stests.core.cache.model import CacheSearchKey
from stests.core.cache.model import StoreOperation
from stests.core.cache.model import StorePartition
from stests.core.cache.ops.utils import cache_op
from stests.core.types.chain import ContractType
from stests.core.types.chain import NamedKey
from stests.core.types.infra import Network
from stests.core.types.infra import NetworkIdentifier
from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext



# Cache partition.
_PARTITION = StorePartition.INFRA

# Cache collections.
COL_NAMED_KEY = "named-key"
COL_NETWORK = "network"
COL_NODE = "node"


@cache_op(_PARTITION, StoreOperation.GET_ONE_FROM_MANY)
def get_named_key(network: str, contract_type: ContractType, name: str) -> CacheItemKey:
    """Decaches domain objects: NamedKey.

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.
    
    """
    return CacheItemKey(
        paths=[
            network,
            COL_NAMED_KEY,
            "A-*",
            contract_type.name,
        ],
        names=[
            name,
        ]
    )


@cache_op(_PARTITION, StoreOperation.GET_MANY)
def get_named_keys(network: typing.Union[NetworkIdentifier, Network, str]) -> CacheSearchKey:
    """Decaches domain objects: NamedKey.

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.
    
    """
    try:
        network = network.name
    except AttributeError:
        pass

    return CacheSearchKey(
        paths=[
            network,
            COL_NAMED_KEY,            
        ]
    )


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_network(network_id: NetworkIdentifier) -> CacheItemKey:
    """Decaches domain object: Network.

    :param network_id: A network identifier.

    :returns: A registered network.
    
    """
    return CacheItemKey(
        paths=[
            network_id.name,
        ],
        names=[
            COL_NETWORK,
        ]
    )


@cache_op(_PARTITION, StoreOperation.GET_MANY)
def get_networks() -> CacheSearchKey:
    """Decaches domain objects: Network.

    :returns: List of registered networks.
    
    """
    return CacheSearchKey(
        paths=[
            "*",
            COL_NETWORK,
        ]
    )


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_node(node_id: NodeIdentifier) -> CacheItemKey:
    """Decaches domain object: Node.
    
    :param node_id: A node identifier.

    :returns: A registered node.

    """
    return CacheItemKey(
        paths=[
            node_id.network.name,
            COL_NODE,
        ],
        names=[
            node_id.label_index,
        ]
    )


def get_node_by_network(network: typing.Union[Network, NetworkIdentifier]) -> Node:
    """Decaches domain object: Node.
    
    :param network: A network.

    :returns: A registered node selected at random from a network's nodeset.

    """
    # Pull operational nodeset.
    nodeset = get_nodes_operational(network) 
    if not nodeset:
        raise ValueError(f"Network {network.name} has no registered operational nodes.")

    # Select random node.
    return random.choice(nodeset)


def get_node_by_network_nodeset(network_id: NetworkIdentifier, node_index: int) -> Node:
    """Decaches domain object: Node.
    
    :param network_id: A network identifier.
    :param node_index: A node index.

    :returns: A registered node.

    """
    # Pull operational nodes.
    nodeset = get_nodes_operational(network_id)
    if not nodeset:
        raise ValueError(f"Network {network_id.name} has no registered operational nodes.")
    
    # Select random if node index unspecified.
    if node_index <= 0 or node_index is None:
        return random.choice(nodeset)

    # Select specific with fallback to random.
    try:
        return nodeset[node_index - 1]
    except IndexError:
        return random.choice(nodeset)


@cache_op(_PARTITION, StoreOperation.GET_MANY)
def get_nodes(network: typing.Union[NetworkIdentifier, Network]=None) -> CacheSearchKey:
    """Decaches domain objects: Node.

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.
    
    """
    return CacheSearchKey(
        paths=[
            "*" if network is None else network.name,
            COL_NODE,
        ]
    )     


def get_nodes_operational(network: typing.Union[NetworkIdentifier, Network]) -> typing.List[Node]:
    """Decaches domain objects: Node (if operational).

    :param network: A pointer to either a network or network identifier.

    :returns: Collection of registered nodes.
    
    """
    nodeset = {i.address: i for i in get_nodes(network) if i.is_operational}

    return list(nodeset.values())


@cache_op(_PARTITION, StoreOperation.SET_ONE)
def set_named_key(named_key: NamedKey) -> CacheItem:
    """Encaches domain object: NamedKey.

    :param network: NamedKey domain object instance to be cached.
    
    :returns: Keypath + domain object instance.

    """
    return CacheItem(
        item_key=CacheItemKey(
            paths=[
                named_key.network,
                COL_NAMED_KEY,
                named_key.label_account_index,
                named_key.contract_type.name,
            ],
            names=[
                named_key.name
            ]
        ),
        data=named_key
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE)
def set_network(network: Network) -> CacheItem:
    """Encaches domain object: Network.

    :param network: Network domain object instance to be cached.
    
    :returns: Keypath + domain object instance.

    """
    return CacheItem(
        item_key=CacheItemKey(
            paths=[
                network.name,
            ],
            names=[
                COL_NETWORK,
            ]
        ),
        data=network,
    )


@cache_op(_PARTITION, StoreOperation.SET_ONE)
def set_node(node: Node) -> CacheItem:
    """Encaches domain object: Node.
    
    :param node: Node domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return CacheItem(
        item_key=CacheItemKey(
            paths=[
                node.network,
                COL_NODE,
            ],
            names=[
                node.label_index,
            ]
        ),
        data=node,
    )
