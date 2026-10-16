import json
import uuid
import time
import functools
import logging
from typing import Dict, Any, Callable
from src.identity import AgentExecutionContext

sec_logger = logging.getLogger("GuardAgentOS.Sandbox")

def enforce_security_boundary(required_scope: str):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(self, context: AgentExecutionContext, *args, **kwargs):
            start_time = time.perf_counter()
            sec_logger.info(f"Interception initiated. Verifying token rights for: '{func.__name__}'")
            
            if required_scope not in context.identity.entitled_scopes:
                sec_logger.critical(f"BOUNDARY VIOLATION: Agent missing scope [{required_scope}].")
                raise PermissionError(f"Access Denied: Missing scope: '{required_scope}'")
            
            if context.accumulated_cost >= context.identity.max_token_budget_per_session:
                raise RuntimeError("Execution Blocked: Session financial budget exhausted.")
                
            result = func(self, context, *args, **kwargs)
            
            execution_time = (time.perf_counter() - start_time) * 1000
            context.latency_profile[func.__name__] = execution_time
            return result
        return wrapper
    return decorator

class IsolatedSecureSandbox:
    @staticmethod
    def validate_parameter_schema(data: Dict[str, Any], expected_schema: Dict[str, type]) -> bool:
        try:
            return all(isinstance(data.get(k), t) for k, t in expected_schema.items())
        except Exception:
            return False

    @enforce_security_boundary(required_scope="write:financial:ledger")
    def append_corporate_ledger(self, context: AgentExecutionContext, parameters: Dict[str, Any]) -> str:
        schema = {"account_id": str, "transaction_amount": float}
        if not self.validate_parameter_schema(parameters, schema):
            raise ValueError("Data Validation Failure: Parameter schema mismatch.")

        if "ORG-UK-CORP" not in context.identity.organization_tenant_id:
            return json.dumps({"error": "Data Separation Boundary Infringement Intercepted."})

        context.accumulated_cost += 0.85
        return json.dumps({"status": "SUCCESS", "ledger_reference": str(uuid.uuid4())})
