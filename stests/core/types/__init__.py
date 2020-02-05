from stests.core.types.enums import AccountStatus
from stests.core.types.enums import AccountType
from stests.core.types.enums import NetworkStatus
from stests.core.types.enums import NetworkType
from stests.core.types.enums import NodeStatus
from stests.core.types.enums import NodeType

from stests.core.types.account import Account
from stests.core.types.generator import GeneratorContext
from stests.core.types.key_pair import KeyPair
from stests.core.types.network import Network
from stests.core.types.node import Node

from stests.core.types.references import AccountReference
from stests.core.types.references import GeneratorReference
from stests.core.types.references import NodeReference
from stests.core.types.references import NetworkReference

from stests.core.types.utils import get_isodatetime_field
from stests.core.types.utils import get_uuid_field


# Domain classes.
CLASSES = {
    Account,
    AccountReference,
    GeneratorContext,
    GeneratorReference,
    KeyPair,
    Network,
    NetworkReference,
    Node,
    NodeReference
}

# Domain enums.
ENUMS = {
    AccountStatus,
    AccountType,
    NetworkStatus,
    NetworkType,
    NodeStatus,
    NodeType,
}

# Domain model.
TYPESET = CLASSES | ENUMS
