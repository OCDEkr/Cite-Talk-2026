# Cisco IOS / IOS XE switch audit: check catalogue and rationale

Read this when you need the *why* behind a finding, need to judge a false positive,
or want to look for things the script can't detect. Check IDs match `scripts/audit_config.py`.

## Contents
1. Threat context: what attackers actually exploit
2. Management plane (MGMT, AUTH, SNMP, SVC, LOG)
3. Control plane (CP, routing auth)
4. Layer 2 (L2)
5. Layer 3 (L3)
6. Correctness bugs (CORR): config that is quietly broken
7. Things only a reviewer can judge (no script check)
8. Change-safety notes for remediation
9. Sources

---

## 1. Threat context

These are being exploited in the wild, so they belong at the top of a report:

| Issue | Config indicator | Why it's urgent |
|---|---|---|
| **Smart Install (CVE-2018-0171)**, CVSS 9.8, CISA KEV | no `no vstack` on classic IOS / early IOS XE; TCP 4786 reachable | Unauthenticated RCE plus config download/replace. Cisco Talos (Aug 2025) reported the FSB-linked group **Static Tundra** mass-exploiting it against unpatched/EoL switches. **Salt Typhoon** used it against US telecoms. Post-exploitation: steal configs, add privileged users, change SNMP communities and TACACS+ settings. |
| **IOS XE WebUI (CVE-2023-20198 + CVE-2023-20273)**, CVSS 10 | `ip http server` / `ip http secure-server` on IOS XE 16/17 without `ip http active-session-modules none` / `ip http secure-active-session-modules none` | Unauthenticated priv-15 account creation then root implant. Tens of thousands of devices implanted in Oct 2023. Disabling the server stops new exploitation but **does not remove an implant**. Look for unknown local `username` lines. |
| **SNMP stack bugs (CVE-2017-6736, CVE-2025-20352)**, both exploited | v1/v2c communities, esp. without ACL; v3 groups without ACL | Crafted SNMP packets → RCE/DoS. Cisco's mitigation for both: restrict SNMP sources by ACL and exclude affected MIBs via views. A guessable community makes it trivially reachable. |
| **Type 7 passwords / RW SNMP** | `password 7`, `key 7`, `snmp-server community X RW` | Leaked configs (backups, tickets, TFTP, configs stolen via the bugs above) hand over credentials. Type 7 decodes instantly; RW SNMP can push a new config. |
| **End-of-life software** | `version 12.x`, early 15.x on 2960/3560/3750 | No more fixes. Static Tundra deliberately targets EoL gear. |

When any of these are present, say so plainly in the executive summary. They matter more than twenty hygiene findings.

Exact-release CVE applicability can't be determined from `version 17.9` alone. Always recommend `show version` + the Cisco Software Checker.

---

## 2. Management plane

**MGMT-03 Smart Install.** Classic IOS 12.2(55)SE+/15.x clients have it on by default. A running-config shows `no vstack` only when disabled. Verify with `show vstack config`. Also block TCP/4786 at the edge.

**MGMT-04/05/06 HTTP server.** Many IOS XE images ship with `ip http server` and `ip http secure-server` in the default config, so they appear even when nobody uses the WebUI. Mitigated only if the matching `active-session-modules none` lines exist for each enabled protocol. If Catalyst Center/DNAC, RESTCONF or a controller depends on HTTPS, keep `secure-server` + `ip http access-class ipv4 <ACL>` + patch; otherwise disable both.

**MGMT-07/08 Telnet.** `transport input telnet`/`all`, or missing on classic IOS (default `all`). Clear-text credentials.

**MGMT-09 vty access-class.** Without it, SSH is reachable from every subnet that can route to any switch IP, including user VLANs. With a Mgmt-vrf use `access-class X in vrf-also`.

**MGMT-10 exec-timeout 0 0.** Abandoned sessions stay logged in forever.

**MGMT-12 SSH v1.** Pin v2. Recommend RSA ≥ 2048 (3072 preferred). The modulus isn't in running-config: `show crypto key mypubkey rsa`.

### AUTH: credentials and AAA

Password types: 0 = cleartext, 7 = reversible obfuscation (decodes instantly), 5 = salted MD5 (crackable), 4 = broken, 8 = PBKDF2-SHA256, 9 = scrypt (preferred). Type 6 = AES-reversible with master key (acceptable for *keys* the device must send: TACACS/RADIUS/OSPF).

- **AUTH-01** `enable password` → `enable algorithm-type scrypt secret`.
- **AUTH-04** type 7 anywhere: assume anyone who has seen a backup knows these. Recommend **rotation**, not just re-hashing.
- **AUTH-11** login list without `local`: lockout when servers are unreachable. Local is only tried on server *error*, not on rejection, so adding it barely weakens security.
- **AUTH-12** `none` in a method list = unauthenticated access when servers are down.
- **AUTH-18** `no login` on vty = no authentication.
- **AUTH-19** shared line passwords: no accountability or individual revocation.
- **AUTH-20** `privilege level 15` on vty bypasses enable.
- **AUTH-21** console with no login: physical/console-server access gives a full shell.
- Unknown privileged `username` entries (e.g. `cisco_tac_admin`, `cisco_support`, random 8-char names) are an **indicator of compromise** after CVE-2023-20198 / Smart Install exploitation. Flag them for the owner to verify.

### SNMP
- **SNMP-01** `public`/`private`/vendor defaults: scanned for constantly.
- **SNMP-02** RW community: CISCO-CONFIG-COPY-MIB can TFTP the config out or push a new one.
- **SNMP-03** no ACL: the token after RO/RW is the ACL (`snmp-server community X RO 10`).
- **CORR-02** ACL name that isn't defined → IOS accepts it and **filters nothing**.
- **SNMP-04/05** prefer `snmp-server group G v3 priv access ACL` + `snmp-server user u G v3 auth sha ... priv aes 256 ...`.
- Unexpected `snmp-server host` / communities pointing outside the org are a known Static Tundra persistence trick, so flag them.

### SVC: legacy services
Small servers, finger, BOOTP, PAD, `service config` (loads config from network at boot, so a rogue TFTP server can configure the switch), source routing, `tftp-server flash:...`, rsh/rcp. Mostly off by default on 12.2+/15.x but still show up on old or copy-pasted configs.

CDP/LLDP: informational. Keep on infrastructure links and phone ports (voice VLAN discovery). Don't present as a big risk.

### LOG
Remote syslog, datetime timestamps, NTP (ideally authenticated), `archive / log config`, login banner. On IOS XE with Mgmt-vrf, `logging host X vrf Mgmt-vrf` and `ntp server vrf Mgmt-vrf` are correct forms. Don't flag them as malformed.

---

## 3. Control plane

**CP-01 CoPP.** Catalyst 9000 has a non-removable default `system-cpp-policy`. Older Catalysts (2960/3560/3750) have limited CoPP. Matters most on L3 distribution/core.

**Routing protocol auth (L3-05/06/07).** OSPF/EIGRP without auth + no `passive-interface default` means any host on a user SVI can form an adjacency and inject a default route. A real issue on distribution switches whose `network` statements cover user VLAN ranges (e.g. `network 10.20.0.0 0.0.255.255 area 0`).

---

## 4. Layer 2

**L2-01 VTP.** A server/client-mode switch with no password joins any domain it hears. A switch with a higher revision number (an old lab switch plugged back in) overwrites the VLAN database domain-wide, deleting VLANs and dropping every access port in them. On classic IOS, **VTP mode/domain live in vlan.dat and are NOT in running-config**, so absence means "unknown, probably server". Ask for `show vtp status`. Recommend `transparent`/`off`, or VTPv3 with primary server + password.

**L2-03 DTP.** A physical L2 port with no `switchport mode` is `dynamic auto` on most Catalysts (`dynamic desirable` on some old ones). An attacker sends DTP and gets a trunk to every VLAN (switch spoofing). Fix: `switchport mode access` + `switchport nonegotiate`; shut unused ports.

**L2-05 native VLAN.** Double-tagging: the attacker's outer tag (native) is stripped by the first trunk, and the inner tag delivers the frame into another VLAN (one-way). Mitigation: native = unused VLAN, or `vlan dot1q tag native`. Must match both ends. AP trunks with native = AP mgmt VLAN are common and intentional, so note them at lower severity.

**L2-06 trunk allowed list.** Limits blast radius and flooding.

**L2-07/09 VLAN 1.** Every unconfigured port defaults to it. Management in VLAN 1 means any forgotten port lands in the management network.

**L2-10 unused ports.** Link state isn't in the config. Heuristic: enabled, no description, default VLAN. Ask for `show interfaces status`.

**L2-12/13 BPDU Guard / Loop Guard / Root Guard.** BPDU Guard on edge ports. Root guard on distribution downlinks to access switches. The distribution pair should hold the lowest `spanning-tree vlan X priority`. Root priority set on an access switch is a design smell.

**L2-14 Port security / 802.1X.** 802.1X/MAB (`authentication port-control auto`, `mab`, `dot1x pae authenticator`, or IBNS 2.0 `access-session`) is the modern answer; port-security is the fallback.

**L2-16/17 DHCP snooping, DAI, IPSG.** Snooping stops rogue DHCP; DAI (needs the binding table) stops ARP spoofing; IP Source Guard (`ip verify source`) stops IP spoofing. Rollout order: snooping → trust uplinks → verify bindings → DAI → IPSG.

**L2-18 IPv6 FHS.** If IPv6 is enabled anywhere, rogue RAs can MITM even "IPv4-only" hosts.

---

## 5. Layer 3
- **L3-01 proxy-arp**, **L3-02 redirects/unreachables**: hygiene.
- **L3-03 `ip directed-broadcast`**: smurf amplification. Off by default since 12.0, so if present someone enabled it (often for Wake-on-LAN). Suggest a scoped alternative.
- **L3-04 HSRP/VRRP without auth**: any host can claim the gateway with higher priority + preempt → MITM.
- **SVIs with no ACL between zones** (SERVERS, PCI, CAMERAS, OT VLAN names with no `ip access-group`) is a design question. Mention it.

---

## 6. Correctness bugs (CORR)

Config that looks fine in a skim but doesn't do what the author intended or breaks things. Often the most valuable findings, because nobody knows about them.

| ID | Pattern | What actually happens |
|---|---|---|
| CORR-01 | vty `access-class NAME in`, NAME undefined | No filtering; every source allowed. Usually a typo or rename. |
| CORR-02 | SNMP community ACL undefined | No filtering. |
| CORR-03 | `ntp access-group` ACL undefined | Ineffective. |
| CORR-04 | `ip dhcp snooping` without `ip dhcp snooping vlan` | Does nothing. |
| CORR-05 | snooping on VLANs, uplink not `ip dhcp snooping trust` | Real server's OFFER/ACK dropped; clients slowly lose leases. Classic outage-after-hardening. Less severe on a distribution switch that *is* the relay, but downlink trunks to snooping access switches may need trust. |
| CORR-07 | Option 82 inserted by default | Upstream relays/servers may drop requests. `no ip dhcp snooping information option` is common. |
| CORR-08/09 | DAI without snooping / no trusted uplink | Every dynamic host's ARP dropped / gateway unreachable. |
| CORR-10 | `ip access-group NAME` NAME undefined | Interface unfiltered. |
| CORR-11 | `ip default-gateway` with `ip routing` | Ignored. |
| CORR-12 | Duplicate IPs | Conflict. |
| CORR-13 | Access/voice VLAN not in VLAN DB | Port "inactive", no forwarding. Reliable only when VLANs are in config (VTP transparent/off or IOS XE). |
| CORR-14 | Trunk native VLAN undefined | Native traffic dropped. |

Look for these by eye too:
- **Port-channel vs member mismatch** (allowed VLANs, native, mode) → members suspended.
- **`switchport trunk allowed vlan X`** in a change script where `add` was meant → wipes the list.
- **vty/SNMP ACLs that permit user subnets** or end in `permit any`, defeating the purpose.
- **`aaa group server` referencing a `server name` with no matching `tacacs server`/`radius server` block**; or `ip tacacs/radius source-interface` / VRF mismatch → server rejects the device (NAS IP mismatch).
- **Mgmt-vrf mismatch**: management in Mgmt-vrf but AAA/logging/NTP servers configured without `vrf Mgmt-vrf` (or the AAA group missing `ip vrf forwarding Mgmt-vrf`) → nothing reaches the server.
- **STP root on an access switch.**
- **Authorization lists without `if-authenticated`/`local`** → users rejected when servers are down.

---

## 7. Things only a reviewer can judge

- **Device role.** Infer from hostname (ACC/IDF/DIST/CORE), interface mix, `ip routing`, routing protocols, STP priority. L2-edge findings weigh more on access switches; routing-auth findings weigh more on distribution/core.
- **Compensating controls.** 802.1X on all ports reduces DTP/port-security risk; a management VRF with no user routing reduces vty-ACL urgency (still recommend it).
- **Intent signals.** Descriptions (AP-, PHONE-, SERVER-, UPLINK-) tell you what a port should be.
- **Signs of compromise.** Unknown privileged users, SNMP hosts/communities pointing outside the org, `ip http` re-enabled on an otherwise hardened config, odd `event manager applet` (EEM persistence), `tftp-server` lines, GRE `interface Tunnel` on an access switch, `monitor session` sending ERSPAN to a remote IP. Flag them as "investigate". Don't present them as proven compromise.
- **Partial configs.** If sections are missing (no `line vty`, no `hostname`), say so and don't claim things are absent.

---

## 8. Change-safety notes

- `no ip http server`/`secure-server`: breaks WebUI, possibly Catalyst Center/DNAC, RESTCONF. Check with the owner.
- New vty `access-class`: apply from a permitted source, keep console access, consider `reload in 10` as a safety net, then `reload cancel`.
- AAA changes: keep a second session open; add `local` fallback *before* touching servers.
- DHCP snooping/DAI: trust uplinks *first*, enable per VLAN, watch `show ip dhcp snooping statistics`.
- Native VLAN: change both ends in the same window.
- `switchport trunk allowed vlan`: use `add`/`remove`.
- `vtp mode transparent`: safe and immediate; VLANs stay and appear in running-config afterwards.
- `no vstack`: safe unless Smart Install zero-touch is actually used.

---

## 9. Sources
- Cisco advisory cisco-sa-20180409-smi (CVE-2018-0171); Cisco Talos "Static Tundra" (Aug 2025); Splunk CVE-2018-0171 detection guide.
- Cisco advisory cisco-sa-iosxe-webui-privesc-j22SaA4z (CVE-2023-20198/20273); CISA, Rapid7, Unit 42 write-ups.
- Cisco SNMP advisories (CVE-2017-6736, CVE-2025-20352).
- CIS Cisco IOS XE 17.x Benchmark; DISA STIG Cisco IOS XE Switch (NDM/L2S/RTR); Cisco IOS XE hardening guide.
