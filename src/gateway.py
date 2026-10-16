import re
import logging

sec_logger = logging.getLogger("GuardAgentOS.Gateway")

class EnterpriseAIGateway:
    """Inline threat firewall scrubbing prompt injection structures and regulatory exfiltrations."""
    
    def __init__(self):
        self.malicious_intent_patterns = [
            re.compile(r"(?i)ignore\s+previous\s+instructions"),
            re.compile(r"(?i)system\s+prompt\s+override"),
            re.compile(r"(?i)expose\s+internal\s+logic"),
            re.compile(r"(?i)unrestricted\s+root\s+access"),
            re.compile(r"(?i)base64\s+decode\s+the\s+following")
        ]
        
        self.dlp_patterns = {
            "UK_NATIONAL_INSURANCE": re.compile(r"\b[A-CEGHJ-PR-TW-Z][A-Z]\s*\d{6}\s*[A-D]\b"),
            "ENTERPRISE_API_SECRET": re.compile(r"(?i)sk_live_[0-9a-zA-Z]{32,48}")
        }

    def evaluate_inbound_prompt(self, prompt: str) -> bool:
        for pattern in self.malicious_intent_patterns:
            if pattern.search(prompt):
                sec_logger.error("THREAT DETECTED: Inbound prompt vector matched adversarial structure.")
                return False
        return True

    def sanitize_outbound_payload(self, raw_output: str) -> str:
        sanitized = raw_output
        for classification, pattern in self.dlp_patterns.items():
            sanitized = pattern.sub(f"[CLASSIFIED_{classification}_REDACTED]", sanitized)
        return sanitized
