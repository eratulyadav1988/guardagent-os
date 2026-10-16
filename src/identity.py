from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass(frozen=True)
class AgentMachineIdentity:
    """Implements non-human identity (NHI) scoping mechanisms for autonomous agents."""
    agent_urn: str
    organization_tenant_id: str
    entitled_scopes: List[str]
    max_token_budget_per_session: float
    cryptographic_nonce: str

@dataclass
class AgentExecutionContext:
    """Maintains state persistence and runtime metrics for auditability."""
    session_id: str
    identity: AgentMachineIdentity
    execution_chain_log: List[Dict[str, Any]] = field(default_factory=list)
    accumulated_cost: float = 0.0
    latency_profile: Dict[str, float] = field(default_factory=dict)
