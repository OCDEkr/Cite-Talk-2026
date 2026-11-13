---
name: cisco-ios-config-audit
description: Security and misconfiguration audit of Cisco IOS / IOS XE switch configurations (Catalyst 2960/3560/3750/3850/9200/9300/9500 etc.). Finds actively-exploited exposures (Smart Install/vstack, IOS XE WebUI CVE-2023-20198, SNMP), weak credentials (type 7/5, enable password, telnet), missing AAA/vty ACLs, Layer-2 attack surface (DTP, VTP, native VLAN 1, DHCP snooping/DAI, BPDU guard), and correctness bugs like ACLs that are referenced but never defined. Produces a severity-ranked report with evidence lines and remediation commands. Use this whenever the user shares or points to a Cisco running-config / startup-config / "show run" output, asks to harden, review, audit or check a Cisco switch, asks "is this config secure", mentions CIS/STIG compliance for Cisco switches, or wants to compare several switch configs, even if they only paste a snippet and don't say "audit".
---

# Cisco IOS switch config audit

You're acting as a senior network security engineer reviewing a switch config. The goal is a report the switch owner can act on: what's dangerous, why, how sure you are, and the exact commands to fix it without causing an outage.

## Workflow

1. **Get the config into a file.** If the user pasted it, save it to a scratch file first. Multiple configs are fine: the script takes several paths.

2. **Run the deterministic checker** (it covers ~70 checks consistently and masks secrets):
   ```bash
   python3 <skill-dir>/scripts/audit_config.py <config> [<config> ...]          # markdown
   python3 <skill-dir>/scripts/audit_config.py <config> --json                  # structured
   ```
   Treat its output as a *first pass*, not the answer. Findings tagged `[verify]` or `[likely]` depend on platform defaults or state not visible in the config.

3. **Read the config yourself.** The script misses context-dependent problems. In particular:
   - Infer the **switch role** (access / distribution / core / standalone) from hostname, port mix, `ip routing`, routing protocols and STP priorities. Use it to weight severities.
   - Look for the "by eye" items in `references/checks.md` §6–7: port-channel/member mismatches, AAA server-name or VRF mismatches, permissive ACL *contents*, STP root on an access switch, and **indicators of compromise** (unknown priv-15 users, odd SNMP hosts, EEM applets, ERSPAN, tunnels).
   - Drop or downgrade script findings that context makes wrong (e.g. AP trunk with a deliberate native VLAN; DHCP snooping "no trusted ports" on the switch that *is* the relay).

   Consult `references/checks.md` for rationale, false-positive guidance and change-safety notes whenever a finding's severity or fix isn't obvious.

4. **Write the report** using the structure below.

## Severity guide

- **Critical**: remotely exploitable now or credentials effectively public: Smart Install likely on, IOS XE HTTP server on, `public`/`private`/RW SNMP without ACL, `no login`, AAA `none`.
- **High**: direct path to compromise or full-VLAN access: telnet, no vty ACL, undefined ACL that silently permits all, type 7/cleartext secrets, DTP-dynamic user ports, VTP server without password, EoL software, outage-causing bugs (snooping/DAI with no trusted uplink).
- **Medium**: meaningful attack surface or missing detection: native VLAN 1, VLAN 1 usage, no DHCP snooping/DAI, no syslog/NTP, HSRP/OSPF without auth, no AAA, lockout risks.
- **Low / Info**: hygiene and defence in depth.

Adjust for context and say why when you do. A Critical on an isolated lab switch is still worth stating, but note the reduced exposure.

## Report structure

```
# Cisco switch config audit: <hostname>
**Platform/version:** <from config> · **Inferred role:** <role + 1-line reason> · **Date:** <today>

## Executive summary
2–4 sentences: overall posture, the few things to fix first, and any actively-exploited exposure
or sign of compromise stated plainly.
Severity counts table (Critical/High/Medium/Low).

## Priority actions
Numbered list (max ~7) of what to do first, grouped where one change fixes several findings.

## Findings
For each (Critical → Low), sorted by severity:
### [SEVERITY] <ID> <title>
- **Evidence:** config line(s) with line numbers (secrets masked)
- **Risk:** why it matters on *this* switch (attack or failure scenario, one or two sentences)
- **Fix:** exact IOS commands
- **Confidence:** confirmed / likely / needs verification (+ the show command to confirm)
Group repetitive per-port findings into one finding with the port list.

## Needs verification
Show commands to run on the device to resolve uncertain items (show version, show vstack config,
show vtp status, show interfaces status, show crypto key mypubkey rsa, show policy-map control-plane ...).

## Remediation config
One consolidated, copy-pasteable config block ordered for safe application, with comments flagging
steps that can lock you out or break traffic (vty ACL, AAA, DHCP snooping/DAI, native VLAN, HTTP server).
Use placeholders like <MGMT-ACL>, <SYSLOG-IP>. Never invent real addresses or secrets.

## What's done well
Brief: credit good controls so the owner knows what to keep.
```

For several configs, write one section per device, then a short cross-device table of shared issues (e.g. "SNMP RW on 3/3 switches").

If the user asked a narrow question ("is SNMP OK on this?"), answer that directly first, then mention any Critical findings elsewhere in a sentence or two. Don't bury them, and don't produce the full report unasked.

## Handling secrets

Configs contain credentials. Keep them masked in your report (the script does this by default). Don't decode type 7 strings into the output, even though it's trivial. Say they're reversible and must be rotated. Only use `--show-secrets` if the user explicitly asks.

## Limits to state honestly

A running-config can't show the exact software release, link state, VTP state on classic IOS, RSA key size, or whether a CVE's vulnerable feature is reachable through upstream ACLs. Say so where it matters instead of guessing, and point to the show command that settles it. For CVE exposure by release, point to the Cisco Software Checker rather than asserting a version is or isn't vulnerable.
