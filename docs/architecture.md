# GuardAgent-OS Core System Topology

```mermaid
graph TD
    A[Untrusted Inbound Agent Intent] -->|Step 1: Perimeter Scan| B(Enterprise AI Gateway Firewall)
    B -->|Check 1: Look for Prompts Injections| C{Threat Discovered?}
    C -->|Yes| D[Block Process & Route to Security Logs]
    C -->|No| E[GuardAgent Orchestration Routing Engine]
    
    E -->|Step 2: Bind System State Context| F[Verify Non-Human Machine Identity Scope]
    F -->|Step 3: Trigger Token Authentication Check| G[@enforce_security_boundary Decorator Interception]
    
    G -->|Passes Policy Thresholds| H[Isolated Secure Tool Sandbox Executions]
    H -->|Executes Data Action Legitimate Run| I[Downstream Generation Models Engine Layer]
    
    I -->|Step 4: Output Validation Scan Passing| J(Outbound DLP Semantic Filter Component)
    J -->|Scrub UK PII & Enterprise Secret Keys| K[Deliver Secured Clean Payload Data Output]
```
