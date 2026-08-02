# Detection Notes Template

## Detection Goal

Describe the suspicious behavior the detection should identify.

## Data Sources

- Windows Event Logs
- Firewall logs
- DNS logs
- Proxy logs
- VPN logs
- Endpoint logs
- Cloud audit logs
- Email security logs

## Logic

Explain the detection logic in plain language.

## Example Query

```text
Add SPL, KQL, SQL, Sigma-style logic, or pseudocode here.
```

## Useful Fields

- timestamp
- username
- hostname
- source_ip
- destination_ip
- event_id
- process_name
- command_line
- action

## False Positives

List normal activity that may trigger the detection.

## Triage Steps

1. Confirm the affected user or host.
2. Check related events before and after the alert.
3. Review source and destination details.
4. Look for repeated activity or escalation.
5. Document evidence and next action.

## Response Guidance

- Escalate when:
- Contain when:
- Close as benign when:

## References

- MITRE ATT&CK:
- Vendor documentation:
- Related research: