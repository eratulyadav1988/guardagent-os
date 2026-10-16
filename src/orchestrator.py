import json
import uuid
import time
import logging
from src.identity import AgentMachineIdentity, AgentExecutionContext
from src.gateway import EnterpriseAIGateway
from src.sandbox import IsolatedSecureSandbox

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [SIEM] - %(name)s - %(message)s')

class GuardAgentOrchestrator:
    def __init__(self, machine_identity: AgentMachineIdentity):
        self.gateway = EnterpriseAIGateway()
        self.sandbox = IsolatedSecureSandbox()
        self.session_context = AgentExecutionContext(
            session_id=f"sess_{uuid.uuid4().hex[:12]}",
            identity=machine_identity
        )

    def process_agent_execution_cycle(self, user_intent: str, proposed_tool_inputs: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.perf_counter()
        
        if not self.gateway.evaluate_inbound_prompt(user_intent):
            return {"status": "BLOCKED", "reason": "Threat Signal Verified."}

        try:
            tool_output = self.sandbox.append_corporate_ledger(self.session_context, proposed_tool_inputs)
            self.session_context.execution_chain_log.append({"action": "append_corporate_ledger", "status": "success"})
        except Exception as err:
            return {"status": "EXECUTION_ABORTED", "reason": str(err)}

        raw_model_generation = (
            f"Transaction synchronized successfully. Ref: {tool_output}. "
            f"Operator National Insurance reference is QQ123456A. "
            f"System connection key: [REDACTED_BY_PLATFORM_INTEGRATION_KEY]"

        )

        clean_payload = self.gateway.sanitize_outbound_payload(raw_model_generation)
        total_latency = (time.perf_counter() - start_time) * 1000
        self.session_context.latency_profile["total_lifecycle_loop"] = total_latency

        return {
            "status": "SECURED_SUCCESS",
            "session_id": self.session_context.session_id,
            "data": clean_payload,
            "security_metrics": {
                "accumulated_cost": f"£{self.session_context.accumulated_cost:.2f}",
                "internal_tool_latency_ms": f"{self.session_context.latency_profile.get('append_corporate_ledger', 0.0):.2f}ms",
                "total_security_overhead_ms": f"{self.session_context.latency_profile.get('total_lifecycle_loop', 0.0):.2f}ms"
            }
        }

if __name__ == "__main__":
    valid_nhi = AgentMachineIdentity(
        agent_urn="urn:uk:enterprise:agent:finance:01",
        organization_tenant_id="ORG-UK-CORP-LONDON-HQ",
        entitled_scopes=["write:financial:ledger"],
        max_token_budget_per_session=10.00,
        cryptographic_nonce="nonce_sec_994823"
    )
    orchestrator = GuardAgentOrchestrator(machine_identity=valid_nhi)
    print("\n--- RUNNING ARCHITECTURE SYSTEM INTEGRITY DEMO ---")
    res = orchestrator.process_agent_execution_cycle(
        user_intent="Commit standard end-of-month balance declarations.",
        proposed_tool_inputs={"account_id": "ACC-LONDON-2026", "transaction_amount": 894500.00}
    )
    print(json.dumps(res, indent=2))
