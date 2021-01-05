from stests.core.types.orchestration import ExecutionContext
from stests.generators.wg_210 import args
from stests.generators.wg_210 import p1s1_set_accounts
from stests.generators.wg_210 import p1s2_delegate



# Workload custom args type.
Arguments = args.Arguments

# Workload command line args.
ARGS = args.ARGS

# Workload description.
DESCRIPTION = "Submits a deploy delegating an amount of tokens (in motes) to a validator for staking purposes."

# Workflow phases/steps.
PHASES = (
    (p1s1_set_accounts, p1s2_delegate, ),
)

# Workload type.
TYPE = "WG-210"

# Workload typeset - registered when encoder.initialise is invoked.
TYPE_SET = {
    Arguments,
}
