import typing

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.clx.defaults import CLX_TX_FEE
from stests.core.types.chain import Account
from stests.core.types.chain import AccountType
from stests.core.types.chain import ContractType
from stests.core.types.chain import DeployType
from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.core import factory



# Queue to which messages will be dispatched.
_QUEUE = "workflows.generators.accounts"

# Account index: network faucet.
ACC_NETWORK_FAUCET = 0


@dramatiq.actor(queue_name=_QUEUE)
def do_create_account(ctx: ExecutionContext, index: int, typeof: AccountType):
    """Creates an account for use during the course of a simulation.

    :param ctx: Execution context information.
    :param index: Run specific account index.
    :param typeof: Account type.

    """
    account = factory.create_account_for_run(ctx, index=index, typeof=typeof)
    cache.state.set_account(account)


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_account(
    ctx: ExecutionContext,
    cp1_index: int,
    cp2_index: int,
    amount: int,
    ):
    """Funds an account by transfering CLX transfer between 2 counterparties.

    :param ctx: Execution context information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    :param amount: Amount to be transferred.
    
    """
    # Set counterparties.
    if cp1_index == ACC_NETWORK_FAUCET:
        network_id = factory.create_network_id(ctx.network)
        network = cache.infra.get_network(network_id)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        cp1 = network.faucet
    else:
        cp1 = cache.state.get_account_by_index(ctx, cp1_index)
    cp2 = cache.state.get_account_by_index(ctx, cp2_index)
    
    # Transfer CLX from cp1 -> cp2.
    _transfer(ctx, cp1, cp2, amount)
    

@dramatiq.actor(queue_name=_QUEUE)
def do_refund(ctx: ExecutionContext, cp1_index: int, cp2_index: int):
    """Performs a refund ot funds between 2 counterparties.

    :param ctx: Execution context information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    
    """
    # Set counterparties.
    cp1 = cache.state.get_account_by_index(ctx, cp1_index)
    if cp2_index == ACC_NETWORK_FAUCET:
        network_id = factory.create_network_id(ctx.network)
        network = cache.infra.get_network(network_id)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        cp2 = network.faucet
    else:
        cp2 = cache.state.get_account_by_index(ctx, cp2_index)

    # Set amount.
    cp1_balance = clx.get_account_balance(ctx, cp1)
    amount = cp1_balance - CLX_TX_FEE
    if amount <= 0:
        logger.log_warning(f"Counter party 1 (account={cp1.index}) does not have enough CLX to pay refund transaction fee, balance={cp1_balance}.")
        return

    # Transfer CLX from cp1 -> cp2.
    _transfer(ctx, cp1, cp2, amount)


def _transfer(ctx, cp1, cp2, amount):
    """Executes transfer between 2 counterparties.
    
    """
    # Set contract.
    contract_type = ContractType.TRANSFER_U512 if ctx.run_type == "WG-100" else ContractType.TRANSFER_U512_STORED
    contract = clx.contracts.get_contract(contract_type)

    # Transfer CLX from cp1 -> cp2.    
    node, deploy_hash = contract.transfer(ctx, cp1, cp2, amount)

    # Update cache.
    cache.state.set_deploy(factory.create_deploy_for_run(
        ctx=ctx, 
        account=cp1,
        node=node, 
        deploy_hash=deploy_hash, 
        typeof=DeployType.TRANSFER
        ))
    cache.state.set_transfer(factory.create_transfer(
        ctx=ctx,
        amount=amount,
        asset="CLX",
        cp1=cp1,
        cp2=cp2,
        deploy_hash=deploy_hash,
        ))
    if cp1.is_run_account:
        cache.state.decrement_account_balance(cp1, amount)
    if cp2.is_run_account:
        cache.state.increment_account_balance(cp2, amount)
