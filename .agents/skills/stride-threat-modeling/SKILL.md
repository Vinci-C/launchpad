---
name: stride-threat-modeling
description: Run a STRIDE threat modeling analysis on the current architecture and code.
---

# STRIDE Threat Modeling

Use this skill when you need to perform a security analysis of a system or component using the STRIDE methodology.

## Instructions

1. **Spoofing:** Can an attacker masquerade as a legitimate user or system?
2. **Tampering:** Can an attacker modify data in transit or at rest?
3. **Repudiation:** Can an attacker deny performing an action?
4. **Information Disclosure:** Can an attacker access confidential data?
5. **Denial of Service:** Can an attacker impact the availability of the system?
6. **Elevation of Privilege:** Can an attacker gain elevated access rights?

When invoked, generate a markdown report analyzing the current codebase or architecture against these six categories, identifying potential threats and recommending mitigations.
