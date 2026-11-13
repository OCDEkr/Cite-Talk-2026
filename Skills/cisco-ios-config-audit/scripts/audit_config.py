#!/usr/bin/env python3
"""
Deterministic first-pass auditor for Cisco IOS / IOS XE switch running-configs.

Usage:
    python3 audit_config.py <config-file> [<config-file> ...] [--json] [--show-secrets]

It parses the config into global lines + indented blocks, classifies interfaces,
and runs a catalogue of checks (IDs match references/checks.md). Output is a
markdown findings list (default) or JSON. Secrets are masked unless --show-secrets.

The script is a *first pass*: it is deliberately a little noisy on
"verify"-type findings, because a human/LLM reviewer should apply context
(switch role, compensating controls) on top. It never contacts the device.
"""
import json
import re
import sys
from collections import OrderedDict

SEV_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}

PHYS_RE = re.compile(
    r"^(FastEthernet|GigabitEthernet|TenGigabitEthernet|TwoGigabitEthernet|"
    r"FiveGigabitEthernet|TwentyFiveGigE|FortyGigabitEthernet|HundredGigE|"
    r"Ethernet)\S*$",
    re.I,
)


# --------------------------------------------------------------------------- parsing
class Block:
    def __init__(self, header, lineno):
        self.header = header
        self.lineno = lineno
        self.children = []  # list of (lineno, text) - stripped, nested levels flattened

    def has(self, pattern):
        r = re.compile(pattern, re.I)
        return any(r.search(c) for _, c in self.children)

    def find(self, pattern):
        r = re.compile(pattern, re.I)
        return [(n, c) for n, c in self.children if r.search(c)]

    def first(self, pattern):
        r = re.compile(pattern, re.I)
        for _, c in self.children:
            m = r.search(c)
            if m:
                return m
        return None


NOISE_RE = re.compile(
    r"^(Building configuration|Current configuration|Load for|Time source|"
    r"\S+[#>]\s*(show|sh)\s|end$)",
    re.I,
)


def parse(text):
    """Return (global_lines, blocks). global_lines: list of (lineno, text) for every
    top-level line. blocks: a Block per top-level line, holding its indented children."""
    global_lines = []
    blocks = []
    current = None
    in_banner = None
    for i, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip("\r\n")
        if in_banner:
            if in_banner in line:
                in_banner = None
            continue
        if not line.strip():
            continue
        if line.strip() == "!":
            if not line.startswith(" "):
                current = None
            continue
        if NOISE_RE.match(line.strip()):
            continue
        m = re.match(r"^banner\s+\S+\s+(\^C|\S)", line)
        if m:
            global_lines.append((i, line.strip()))
            delim = m.group(1)
            rest = line[m.end(1):]
            if delim not in rest:
                in_banner = delim
            current = None
            continue
        if line[0] in (" ", "\t"):
            if current is not None:
                current.children.append((i, line.strip()))
            continue
        stripped = line.strip()
        global_lines.append((i, stripped))
        current = Block(stripped, i)
        blocks.append(current)
    return global_lines, blocks


class Config:
    def __init__(self, text, name):
        self.name = name
        self.text = text
        self.glines, self.blocks = parse(text)
        self.interfaces = [b for b in self.blocks if re.match(r"^interface\s", b.header, re.I)]
        self.lines_cfg = [b for b in self.blocks if re.match(r"^line\s", b.header, re.I)]

    def g(self, pattern):
        r = re.compile(pattern, re.I)
        return [(n, l) for n, l in self.glines if r.search(l)]

    def g1(self, pattern):
        r = re.compile(pattern, re.I)
        for n, l in self.glines:
            m = r.search(l)
            if m:
                return n, l, m
        return None

    def blocks_matching(self, pattern):
        r = re.compile(pattern, re.I)
        return [b for b in self.blocks if r.search(b.header)]

    @property
    def hostname(self):
        h = self.g1(r"^hostname\s+(\S+)")
        return h[2].group(1) if h else "(no hostname)"

    @property
    def version(self):
        v = self.g1(r"^version\s+(\S+)")
        return v[2].group(1) if v else None

    def defined_acls(self):
        names = set()
        for _, l in self.glines:
            m = re.match(r"^access-list\s+(\S+)", l, re.I)
            if m:
                names.add(m.group(1))
            m = re.match(r"^ip(?:v6)?\s+access-list\s+(?:standard\s+|extended\s+|role-based\s+)?(\S+)", l, re.I)
            if m and m.group(1).lower() not in ("log-update", "logging", "persistent", "match-local-traffic"):
                names.add(m.group(1))
        return names


# --------------------------------------------------------------------------- helpers
def mask(s, show):
    if show:
        return s
    s = re.sub(r"(snmp-server community\s+)(\S+)", r"\1<redacted>", s, flags=re.I)
    s = re.sub(r"\b((?:secret|password|key-string|key)\s+(?:\d\s+)?)(?!<redacted>)(\S+)",
               lambda m: m.group(1) + "<redacted>", s, flags=re.I)
    return s


def ifname(b):
    return b.header.split(None, 1)[1] if " " in b.header else b.header


def is_shut(b):
    return any(c == "shutdown" for _, c in b.children)


def classify(b):
    """svi, loopback, tunnel, mgmt, routed, access, trunk, dynamic, portchannel-<mode>, other."""
    name = ifname(b)
    low = name.lower()
    if low.startswith("vlan"):
        return "svi"
    if low.startswith("loopback"):
        return "loopback"
    if low.startswith("tunnel"):
        return "tunnel"
    if low.startswith(("appgigabitethernet", "bluetooth", "null")):
        return "other"
    if b.has(r"^vrf forwarding Mgmt") or low in ("fastethernet0", "mgmt0"):
        return "mgmt"
    if b.has(r"^no switchport$"):
        return "routed"
    mode = b.first(r"^switchport mode (\S+)")
    kind = None
    if mode:
        m = mode.group(1).lower()
        kind = {"access": "access", "trunk": "trunk"}.get(m, "dynamic")
    if low.startswith("port-channel"):
        return "portchannel-" + (kind or "dynamic")
    if PHYS_RE.match(name):
        if kind:
            return kind
        if b.has(r"^ip address \d"):
            return "routed"
        return "dynamic"
    return "other"


def summarize_ports(blocks, limit=12):
    names = [ifname(b) for b in blocks]
    if len(names) <= limit:
        return ", ".join(names)
    return ", ".join(names[:limit]) + f", ... (+{len(names) - limit} more)"


# --------------------------------------------------------------------------- checks
class Findings:
    def __init__(self, show_secrets):
        self.items = []
        self.show = show_secrets

    def add(self, cid, sev, title, evidence, fix, confidence="confirmed", note=None):
        if isinstance(evidence, (list, tuple)):
            ev = [mask(f"L{n}: {t}", self.show) for n, t in evidence]
        else:
            ev = [mask(str(evidence), self.show)]
        if len(ev) > 15:
            ev = ev[:15] + [f"... ({len(ev) - 15} more)"]
        self.items.append(OrderedDict(
            id=cid, severity=sev, title=title, confidence=confidence,
            evidence=ev, fix=fix, note=note))


def run_checks(cfg, show_secrets=False):
    F = Findings(show_secrets)
    ver = cfg.version
    major = None
    if ver:
        m = re.match(r"(\d+)\.(\d+)", ver)
        if m:
            major = float(f"{m.group(1)}.{m.group(2).zfill(2)}")
    is_xe = major is not None and major >= 16.0
    vtys = [b for b in cfg.lines_cfg if re.match(r"^line vty", b.header, re.I)]
    cons = [b for b in cfg.lines_cfg if re.match(r"^line con", b.header, re.I)]
    acls = cfg.defined_acls()
    aaa = bool(cfg.g(r"^aaa new-model"))

    all_if = cfg.interfaces
    live = [b for b in all_if if not is_shut(b)]
    acc = [b for b in live if classify(b) == "access"]
    dyn = [b for b in live if classify(b) in ("dynamic", "portchannel-dynamic")]
    trunks = [b for b in live if classify(b) in ("trunk", "portchannel-trunk")]
    # members of a port-channel inherit from the bundle; report on the bundle where possible
    trunks_report = [b for b in trunks if not b.has(r"^channel-group")] or trunks

    # ---------------- MGMT: software / exploited features
    if major is not None and major < 15.0:
        F.add("MGMT-01", "HIGH", f"End-of-life IOS train (version {ver})", cfg.g(r"^version"),
              "Plan refresh; EoL trains get no security fixes. Check exact release in Cisco Software Checker.",
              note="Config shows only the major train; confirm with 'show version'.")
    elif ver:
        F.add("MGMT-02", "INFO", f"Software train {ver}: check exact release against Cisco advisories",
              cfg.g(r"^version"),
              "Run 'show version' and check the release in Cisco Software Checker "
              "(sec.cloudapps.cisco.com/security/center/softwarechecker.x).",
              confidence="verify")

    # Smart Install (CVE-2018-0171, CISA KEV; exploited by Static Tundra / Salt Typhoon)
    if not cfg.g(r"^no vstack"):
        if cfg.g(r"^vstack"):
            F.add("MGMT-03", "CRITICAL", "Smart Install (vstack) explicitly enabled", cfg.g(r"^vstack"),
                  "no vstack   ! and block TCP/4786 at the edge")
        elif major is not None and 16.0 <= major < 17.0:
            F.add("MGMT-03", "MEDIUM", "Smart Install state unknown on IOS XE 16.x ('no vstack' absent)",
                  "No 'no vstack' line", "no vstack   ! verify with 'show vstack config'", confidence="verify",
                  note="Many 16.x releases ship with Smart Install disabled when unused, but some don't. "
                       "CVE-2018-0171 is CISA-KEV and still exploited, so confirm rather than assume.")
        elif major is None or major < 16.0:
            F.add("MGMT-03", "CRITICAL", "Smart Install not disabled ('no vstack' absent)",
                  "No 'no vstack' line. The Smart Install client is ON by default on many Catalyst IOS / early IOS XE releases",
                  "no vstack   ! verify: 'show vstack config' -> 'Oper Mode: Disabled'",
                  confidence="likely",
                  note="CVE-2018-0171 (CVSS 9.8, CISA KEV) is still exploited by state actors (Static Tundra, Salt Typhoon) "
                       "to steal configs and plant persistence. Confirm with 'show vstack config'.")

    # HTTP server / WebUI (CVE-2023-20198 + CVE-2023-20273 on IOS XE)
    http = cfg.g(r"^ip http server")
    https = cfg.g(r"^ip http secure-server")
    if http or https:
        mitig_http = cfg.g(r"^ip http active-session-modules none")
        mitig_https = cfg.g(r"^ip http secure-active-session-modules none")
        exposed = (http and not mitig_http) or (https and not mitig_https)
        if exposed:
            sev = "CRITICAL" if is_xe else "HIGH"
            F.add("MGMT-04", sev,
                  "HTTP/HTTPS management server enabled" + (" (IOS XE WebUI: CVE-2023-20198 class)" if is_xe else ""),
                  http + https,
                  "no ip http server\nno ip http secure-server\n"
                  "! If WebUI/RESTCONF is required: keep only secure-server, add 'ip http access-class ipv4 <MGMT-ACL>', patch.",
                  note=("CVE-2023-20198 was mass-exploited in Oct 2023 (tens of thousands of IOS XE devices implanted). "
                        "Disabling blocks new exploitation; it does not remove an existing implant. Check for unknown local users."
                        if is_xe else "Classic IOS HTTP server has its own history of auth-bypass bugs; disable if unused."))
        if http and not https:
            F.add("MGMT-05", "MEDIUM", "Plain-text HTTP management without HTTPS", http,
                  "no ip http server  (use ip http secure-server if a web UI is needed)")
        if not cfg.g(r"^ip http access-class"):
            F.add("MGMT-06", "MEDIUM", "HTTP server has no access-class restriction", http + https,
                  "ip http access-class ipv4 <MGMT-ACL>")

    # ---------------- AUTH
    ep = cfg.g(r"^enable password")
    es = cfg.g(r"^enable (algorithm-type \S+ )?secret")
    if ep:
        F.add("AUTH-01", "HIGH", "'enable password' used (weak/reversible)", ep,
              "no enable password\nenable algorithm-type scrypt secret <strong-secret>")
    if not es and not ep:
        F.add("AUTH-02", "MEDIUM", "No enable secret configured", "No 'enable secret' line",
              "enable algorithm-type scrypt secret <strong-secret>")
    for n, l in es:
        if re.search(r"enable secret 5 ", l):
            F.add("AUTH-03", "MEDIUM", "Enable secret uses type 5 (MD5) hash", [(n, l)],
                  "enable algorithm-type scrypt secret <strong-secret>   ! type 9")
    t7 = [(n, l) for n, l in cfg.glines if re.search(r"\b(password|key) 7 \S+", l)]
    for b in cfg.blocks:
        t7 += [(n, f"{b.header} -> {c}") for n, c in b.find(r"\b(password|key) 7 \S+")]
    if t7:
        F.add("AUTH-04", "HIGH", "Type 7 (trivially reversible) passwords/keys present", t7,
              "Use 'username X algorithm-type scrypt secret ...'; for server keys use type 6 "
              "('key config-key password-encrypt' + 'password encryption aes'). "
              "Rotate them: anyone who has seen this config can decode type 7 instantly.")
    t0 = [(n, l) for n, l in cfg.glines
          if re.search(r"\bpassword (0 )?\S+$", l) and not re.search(r"password [67] ", l)
          and not l.startswith(("enable", "security passwords"))]
    for b in cfg.blocks:
        t0 += [(n, f"{b.header} -> {c}") for n, c in b.find(r"^(password|key) (0 )?\S+$")
               if not re.search(r"(password|key) [67] ", c)]
    if t0:
        F.add("AUTH-05", "HIGH", "Clear-text passwords/keys in configuration", t0,
              "Replace with secrets (type 8/9) or type 6 keys; service password-encryption is only a stopgap.")
    if not cfg.g(r"^service password-encryption"):
        F.add("AUTH-06", "LOW", "service password-encryption not enabled", "Line absent",
              "service password-encryption   ! obfuscation only; real fix is secrets/AAA")
    for n, l in cfg.g(r"^username\s+\S+.*\bsecret 5 "):
        F.add("AUTH-07", "LOW", "Local user secret uses type 5 (MD5)", [(n, l)],
              "username <u> privilege <p> algorithm-type scrypt secret <pw>")
    for n, l in cfg.g(r"^username\s+(admin|cisco|root|test|user|guest)\b"):
        F.add("AUTH-08", "LOW", "Default/guessable local username", [(n, l)],
              "Use unique named or break-glass accounts; remove generic ones.")
    if not aaa:
        F.add("AUTH-09", "MEDIUM", "AAA not enabled (no 'aaa new-model')", "Line absent",
              "aaa new-model\naaa authentication login default group <TACACS/RADIUS> local\n"
              "aaa authorization exec default group <..> local if-authenticated\n"
              "aaa accounting exec default start-stop group <..>",
              note="No per-user accountability or central revocation; shared line passwords.")
    else:
        authn = cfg.g(r"^aaa authentication login")
        if not authn:
            F.add("AUTH-10", "MEDIUM", "aaa new-model with no login method lists", cfg.g(r"^aaa new-model"),
                  "aaa authentication login default group <SERVERS> local",
                  note="Login falls back to local usernames; with none defined, remote login is impossible.")
        for n, l in authn:
            if re.search(r"group\s+\S+", l) and not re.search(r"\blocal\b|\benable\b|\bline\b", l):
                F.add("AUTH-11", "MEDIUM", "AAA login list has no local fallback (lockout risk)", [(n, l)],
                      l.rstrip() + " local",
                      note="If all TACACS+/RADIUS servers are unreachable, nobody can log in, including during the outage you need to fix.")
            if re.search(r"\bnone\b", l):
                F.add("AUTH-12", "CRITICAL", "AAA method list includes 'none' (login without authentication)", [(n, l)],
                      "Remove 'none' from the method list.")
        if not cfg.g(r"^aaa accounting (exec|commands)"):
            F.add("AUTH-13", "LOW", "No AAA accounting configured", "No 'aaa accounting exec/commands'",
                  "aaa accounting exec default start-stop group <SERVERS>\n"
                  "aaa accounting commands 15 default start-stop group <SERVERS>")
        if authn and not cfg.g(r"^username\s"):
            F.add("AUTH-14", "MEDIUM", "No local break-glass user defined", "No 'username' lines",
                  "username breakglass privilege 15 algorithm-type scrypt secret <pw>")
    if not cfg.g(r"^login block-for"):
        F.add("AUTH-16", "LOW", "No login brute-force protection", "No 'login block-for'",
              "login block-for 120 attempts 5 within 60\nlogin on-failure log\nlogin on-success log")
    if not cfg.g(r"^security passwords min-length"):
        F.add("AUTH-17", "INFO", "No minimum password length enforced", "No 'security passwords min-length'",
              "security passwords min-length 12")

    # ---------------- lines
    for b in vtys:
        ti = b.first(r"^transport input (.+)")
        tval = ti.group(1).strip() if ti else None
        if tval is None:
            F.add("MGMT-07", "MEDIUM", f"{b.header}: no 'transport input' (platform default may allow telnet)",
                  [(b.lineno, b.header)], "transport input ssh", confidence="verify",
                  note="Classic IOS defaults vty to 'all' (telnet included). Check 'show line vty 0' Allowed input.")
        elif re.search(r"\btelnet\b|\ball\b", tval):
            F.add("MGMT-08", "HIGH", f"{b.header}: Telnet permitted (clear-text credentials)",
                  b.find(r"^transport input"), "transport input ssh")
        if tval == "none":
            continue
        ac = b.first(r"^access-class (\S+) in")
        if ac is None:
            F.add("MGMT-09", "HIGH", f"{b.header}: no access-class (remote login reachable from any source)",
                  [(b.lineno, b.header)], "access-class <MGMT-ACL> in vrf-also")
        elif ac.group(1) not in acls:
            F.add("CORR-01", "HIGH",
                  f"{b.header}: access-class '{ac.group(1)}' references an ACL that is not defined",
                  b.find(r"^access-class"),
                  f"Define ACL {ac.group(1)}. An undefined ACL on a vty filters nothing, so all sources are permitted.")
        et = b.first(r"^exec-timeout (\d+)(?: (\d+))?")
        if et and et.group(1) == "0" and et.group(2) in (None, "0"):
            F.add("MGMT-10", "MEDIUM", f"{b.header}: exec-timeout disabled (sessions never time out)",
                  b.find(r"^exec-timeout"), "exec-timeout 10 0")
        if b.has(r"^no login$"):
            F.add("AUTH-18", "CRITICAL", f"{b.header}: 'no login' (no authentication on vty)",
                  b.find(r"^no login"), "login local  (or AAA)")
        elif not aaa and b.has(r"^login$") and b.has(r"^password"):
            F.add("AUTH-19", "MEDIUM", f"{b.header}: shared line password only (no per-user login)",
                  b.find(r"^login$|^password"), "username <u> algorithm-type scrypt secret <pw>\nline vty ...\n login local")
        if b.has(r"^privilege level 15"):
            F.add("AUTH-20", "MEDIUM", f"{b.header}: 'privilege level 15' (users land directly in enable mode)",
                  b.find(r"^privilege level"), "Remove; grant privilege via AAA authorization.")
    for b in cons:
        if b.has(r"^no login$") or (not aaa and not b.has(r"^login") and not b.has(r"^password")):
            F.add("AUTH-21", "MEDIUM", "Console line has no authentication", [(b.lineno, b.header)],
                  "login local  (or AAA method list)",
                  note="Anyone with physical/console-server access gets a shell (and enable, if enable is unprotected).")
        et = b.first(r"^exec-timeout (\d+)(?: (\d+))?")
        if et and et.group(1) == "0" and et.group(2) in (None, "0"):
            F.add("MGMT-10", "LOW", "Console exec-timeout disabled", b.find(r"^exec-timeout"), "exec-timeout 10 0")
    for b in [b for b in cfg.lines_cfg if re.match(r"^line aux", b.header, re.I)]:
        if not b.has(r"^no exec") and not b.has(r"^transport input none"):
            F.add("MGMT-11", "LOW", "AUX line not disabled", [(b.lineno, b.header)], "no exec\ntransport input none")

    sshv = cfg.g1(r"^ip ssh version (\d)")
    if not sshv:
        F.add("MGMT-12", "LOW", "SSH version not pinned to 2", "No 'ip ssh version 2'",
              "ip ssh version 2", confidence="verify",
              note="Recent IOS XE is v2-only; older images accept v1 when unpinned.")
    elif sshv[2].group(1) == "1":
        F.add("MGMT-12", "HIGH", "SSH version 1 configured", [(sshv[0], sshv[1])], "ip ssh version 2")
    if not cfg.g(r"^ip domain[- ]name|^ip domain name"):
        F.add("MGMT-13", "INFO", "No ip domain name (RSA keys/SSH may never have been generated)", "No domain name",
              "ip domain name example.local\ncrypto key generate rsa modulus 3072", confidence="verify")

    # ---------------- SNMP
    comms = cfg.g(r"^snmp-server community\s+\S+")
    for n, l in comms:
        toks = l.split()[2:]
        name = toks[0]
        rest = toks[1:]
        if rest and rest[0].lower() == "view":
            rest = rest[2:]
        rw = bool(rest) and rest[0].upper() == "RW"
        if rest and rest[0].upper() in ("RO", "RW"):
            rest = rest[1:]
        if rest and rest[0].lower() == "ipv6":
            rest = rest[2:]
        acl = rest[0] if rest else None
        if name.lower() in ("public", "private", "cisco", "community", "snmp", "secret", "admin", "default", "write", "read"):
            F.add("SNMP-01", "CRITICAL", f"Default/guessable SNMP community string ('{name}')", [(n, l)],
                  "Remove; migrate to SNMPv3 authPriv. If v2c is unavoidable, use a long random string + ACL.")
        if rw:
            F.add("SNMP-02", "HIGH" if acl else "CRITICAL",
                  "SNMP read-write community" + ("" if acl else " with no ACL"), [(n, l)],
                  "Remove RW communities. RW SNMP can copy/replace the running config (CISCO-CONFIG-COPY-MIB) "
                  "and attackers like Static Tundra abuse it.")
        if not acl:
            F.add("SNMP-03", "HIGH", "SNMP community with no source ACL", [(n, l)],
                  "snmp-server community <str> RO <SNMP-ACL>",
                  note="Restricting SNMP sources is Cisco's primary mitigation for SNMP RCE/DoS bugs "
                       "(e.g. CVE-2017-6736, CVE-2025-20352, both exploited).")
        elif acl not in acls:
            F.add("CORR-02", "HIGH", f"SNMP community references undefined ACL '{acl}' (permits all)", [(n, l)],
                  f"Define the ACL {acl} (or correct the name).")
    if comms and not cfg.g(r"^snmp-server group \S+ v3 priv"):
        F.add("SNMP-04", "MEDIUM", "SNMPv1/v2c in use, no SNMPv3 authPriv", comms,
              "snmp-server group NMS v3 priv access <SNMP-ACL>\n"
              "snmp-server user nms NMS v3 auth sha <..> priv aes 256 <..>")
    for n, l in cfg.g(r"^snmp-server group \S+ v3 (noauth|auth)\b"):
        F.add("SNMP-05", "MEDIUM", "SNMPv3 group without privacy (no encryption)", [(n, l)], "Use 'v3 priv'.")
    for n, l in cfg.g(r"^snmp-server group \S+ v3 "):
        if " access " not in l:
            F.add("SNMP-06", "LOW", "SNMPv3 group without access ACL", [(n, l)], l + " access <SNMP-ACL>")
    for n, l in cfg.g(r"^snmp-server system-shutdown"):
        F.add("SNMP-07", "MEDIUM", "snmp-server system-shutdown allows remote reload via SNMP", [(n, l)],
              "no snmp-server system-shutdown")

    # ---------------- services
    svc = [
        (r"^service (tcp|udp)-small-servers", "SVC-01", "MEDIUM", "TCP/UDP small servers enabled (echo/chargen DoS)",
         "no service tcp-small-servers\nno service udp-small-servers"),
        (r"^(ip finger|service finger)", "SVC-02", "LOW", "Finger service enabled (user enumeration)", "no ip finger"),
        (r"^ip bootp server", "SVC-03", "LOW", "BOOTP server enabled", "no ip bootp server"),
        (r"^service pad", "SVC-04", "LOW", "PAD service enabled", "no service pad"),
        (r"^service config", "SVC-05", "MEDIUM", "'service config' (autoloads config from network/TFTP at boot)",
         "no service config"),
        (r"^ip source-route", "SVC-06", "MEDIUM", "IP source routing enabled", "no ip source-route"),
        (r"^tftp-server ", "SVC-07", "MEDIUM", "Device is a TFTP server (exposes flash/config files)", "no tftp-server ..."),
        (r"^ip (http client|ftp) password", "SVC-08", "LOW", "Stored HTTP/FTP client password", "Remove; use SCP."),
        (r"^ip dns server", "SVC-09", "LOW", "Device acts as DNS server", "no ip dns server"),
        (r"^ip identd", "SVC-10", "LOW", "identd enabled", "no ip identd"),
        (r"^ip rcmd (rcp|rsh)-enable", "SVC-11", "MEDIUM", "rsh/rcp enabled", "no ip rcmd rcp-enable\nno ip rcmd rsh-enable"),
    ]
    for pat, cid, sev, title, fix in svc:
        hits = cfg.g(pat)
        if hits:
            F.add(cid, sev, title, hits, fix)
    if not cfg.g(r"^no cdp run"):
        F.add("SVC-12", "INFO", "CDP enabled globally (discloses model/version/IP to neighbors)", "No 'no cdp run'",
              "Keep on infrastructure links/phones; 'no cdp enable' on untrusted user ports if not needed.",
              confidence="verify")
    if cfg.g(r"^iox|^app-hosting"):
        F.add("SVC-14", "INFO", "IOx/app-hosting enabled (more attack surface)", cfg.g(r"^iox|^app-hosting"),
              "no iox  (if unused)")

    # ---------------- logging / time / banner
    if not cfg.g(r"^logging (host )?\S*\d+\.\d+\.\d+\.\d+|^logging host"):
        F.add("LOG-01", "MEDIUM", "No remote syslog server", "No 'logging host'",
              "logging host <syslog-ip>\nlogging trap informational\nlogging source-interface <mgmt-if>")
    if cfg.g(r"^no logging on$"):
        F.add("LOG-02", "HIGH", "Logging disabled entirely ('no logging on')", cfg.g(r"^no logging on"), "logging on")
    if not cfg.g(r"^logging buffered"):
        F.add("LOG-03", "LOW", "Local buffered logging not sized", "No 'logging buffered'",
              "logging buffered 64000 informational")
    if not cfg.g(r"^service timestamps log datetime"):
        F.add("LOG-04", "LOW", "Log timestamps are uptime-based, not datetime", cfg.g(r"^service timestamps") or "No 'service timestamps'",
              "service timestamps log datetime msec localtime show-timezone\n"
              "service timestamps debug datetime msec localtime show-timezone")
    if not cfg.g(r"^ntp server|^ntp peer|^sntp server"):
        F.add("LOG-05", "MEDIUM", "No NTP server (timestamps unreliable for forensics/certs)", "No 'ntp server'",
              "ntp server <ip>")
    elif not cfg.g(r"^ntp authenticate"):
        F.add("LOG-06", "LOW", "NTP without authentication", cfg.g(r"^ntp server"),
              "ntp authentication-key 1 hmac-sha2-256 <key>\nntp authenticate\nntp trusted-key 1\nntp server <ip> key 1")
    for n, l in cfg.g(r"^ntp access-group \S+ \S+"):
        a = l.split()[3]
        if a not in acls:
            F.add("CORR-03", "MEDIUM", f"NTP access-group references undefined ACL '{a}'", [(n, l)], f"Define ACL {a}")
    if not any(b.has(r"^log config") for b in cfg.blocks_matching(r"^archive")):
        F.add("LOG-07", "LOW", "Configuration change logging not enabled", "No 'archive / log config'",
              "archive\n log config\n  logging enable\n  notify syslog contenttype plaintext\n  hidekeys")
    if not cfg.g(r"^banner (login|motd)"):
        F.add("LOG-08", "LOW", "No login/MOTD warning banner", "No banner",
              "banner login ^C Authorized access only. Activity is monitored. ^C")

    # ---------------- control plane
    if not any(b.has(r"service-policy input") for b in cfg.blocks_matching(r"^control-plane")):
        F.add("CP-01", "LOW", "No Control Plane Policing (CoPP) shown in config",
              "No 'control-plane / service-policy input'",
              "Catalyst 9k applies system-cpp-policy by default (verify 'show policy-map control-plane'); "
              "older platforms need an explicit CoPP policy.", confidence="verify")

    # ---------------- Layer 2
    vtp_mode = cfg.g1(r"^vtp mode (\S+)")
    vtp_pw = cfg.g(r"^vtp password")
    if vtp_mode and vtp_mode[2].group(1).lower() in ("server", "client"):
        if not vtp_pw:
            F.add("L2-01", "HIGH", f"VTP {vtp_mode[2].group(1)} mode without a VTP password",
                  [(vtp_mode[0], vtp_mode[1])],
                  "vtp mode transparent   (or 'vtp mode off', or VTPv3 with password + primary server)",
                  note="A rogue or re-used switch with a higher config revision can wipe or rewrite VLANs domain-wide "
                       "(a 'VTP bomb'). Every port in a deleted VLAN goes inactive.")
        else:
            F.add("L2-02", "LOW", f"VTP {vtp_mode[2].group(1)} mode in use", [(vtp_mode[0], vtp_mode[1])],
                  "Prefer transparent/off unless VTPv3 is deliberately managed.")
    elif not vtp_mode and not cfg.g(r"^vlan \d"):
        F.add("L2-01", "MEDIUM", "VTP mode not visible in config (server is the factory default)", "No 'vtp mode' line",
              "vtp mode transparent", confidence="verify",
              note="On classic IOS, VTP server/client state lives in vlan.dat and is NOT shown in running-config. "
                   "Check 'show vtp status'.")

    if dyn:
        F.add("L2-03", "HIGH", "Ports left in DTP dynamic mode (switch spoofing / VLAN hopping)",
              [(b.lineno, b.header) for b in dyn],
              "On every non-trunk port:\n switchport mode access\n switchport nonegotiate",
              note=f"{len(dyn)} enabled port(s) have no 'switchport mode' or use dynamic mode: {summarize_ports(dyn)}. "
                   "Default 'dynamic auto' lets an attacker host negotiate a trunk and reach every VLAN.")
    tn = [b for b in trunks_report if not b.has(r"^switchport nonegotiate")]
    if tn:
        F.add("L2-04", "LOW", "Static trunks still sending DTP", [(b.lineno, b.header) for b in tn],
              "switchport nonegotiate   (on trunks to non-Cisco/untrusted devices, e.g. APs, servers)")
    nat1 = [b for b in trunks_report if not b.has(r"^switchport trunk native vlan (?!1$)\d+")]
    if nat1 and not cfg.g(r"^vlan dot1q tag native"):
        F.add("L2-05", "MEDIUM", "Trunks use native VLAN 1 (double-tagging VLAN hop)",
              [(b.lineno, b.header) for b in nat1],
              "switchport trunk native vlan <unused VLAN, e.g. 999>\n! or globally: vlan dot1q tag native",
              note=f"Affected: {summarize_ports(nat1)}. Change both ends of each link in the same window, "
                   "or you get a native VLAN mismatch.")
    allall = [b for b in trunks_report if not b.has(r"^switchport trunk allowed vlan")]
    if allall:
        F.add("L2-06", "MEDIUM", "Trunks allow all VLANs (no pruning)", [(b.lineno, b.header) for b in allall],
              "switchport trunk allowed vlan <explicit list>",
              note=f"Affected: {summarize_ports(allall)}. Careful: 'allowed vlan X' REPLACES the list; "
                   "use 'allowed vlan add X' when adding.")
    acc_v1 = [b for b in acc if not b.has(r"^switchport access vlan (?!1$)\d+")]
    if acc_v1:
        F.add("L2-07", "MEDIUM", "Enabled access ports in VLAN 1", [(b.lineno, b.header) for b in acc_v1],
              "switchport access vlan <user-vlan>  (or shutdown + park in an unused VLAN)",
              note=f"Affected: {summarize_ports(acc_v1)}.")
    for b in [b for b in all_if if ifname(b).lower() == "vlan1"]:
        if b.has(r"^ip address \d") and not is_shut(b):
            F.add("L2-09", "MEDIUM", "Management IP on VLAN 1 SVI",
                  [(b.lineno, b.header)] + b.find(r"^ip address"),
                  "Move management to a dedicated VLAN; shut interface Vlan1.",
                  note="VLAN 1 is the default for every port and carries CDP/VTP/DTP, so any unconfigured port lands next to management.")
    idle = [b for b in acc_v1 + dyn if not b.has(r"^description")]
    if len(idle) >= 2:
        F.add("L2-10", "MEDIUM", "Enabled ports with no description/VLAN (probably unused, not shut down)",
              [(b.lineno, b.header) for b in idle],
              "interface range <unused>\n switchport mode access\n switchport access vlan <parking-vlan>\n shutdown",
              confidence="verify",
              note=f"{len(idle)} port(s). Confirm with 'show interfaces status | i notconnect'.")
    stp_mode = cfg.g1(r"^spanning-tree mode (\S+)")
    if not stp_mode or stp_mode[2].group(1) == "pvst":
        F.add("L2-11", "LOW", "Legacy PVST+ spanning tree (slow convergence)",
              [(stp_mode[0], stp_mode[1])] if stp_mode else "No 'spanning-tree mode'",
              "spanning-tree mode rapid-pvst")
    glob_bpdu = cfg.g(r"^spanning-tree portfast (edge )?bpduguard default")
    if acc and not glob_bpdu:
        no_guard = [b for b in acc if not b.has(r"^spanning-tree bpduguard enable")]
        if no_guard:
            F.add("L2-12", "MEDIUM", "Access ports without BPDU Guard", [(b.lineno, b.header) for b in no_guard],
                  "spanning-tree portfast edge default\nspanning-tree portfast edge bpduguard default",
                  note=f"Affected: {summarize_ports(no_guard)}. A rogue switch can cause a loop or take over as root bridge.")
    if trunks and not cfg.g(r"^spanning-tree loopguard default"):
        F.add("L2-13", "INFO", "Loop Guard not enabled globally", "No 'spanning-tree loopguard default'",
              "spanning-tree loopguard default", confidence="verify")
    if acc and not any(b.has(r"^switchport port-security|^authentication|^access-session|^dot1x|^mab") for b in acc):
        F.add("L2-14", "LOW", "No port security or 802.1X/MAB on access ports",
              [(b.lineno, b.header) for b in acc[:3]],
              "Prefer 802.1X/MAB. Otherwise: switchport port-security / maximum 2 / violation restrict / aging time 10",
              confidence="verify")
    if acc and not any(b.has(r"^storm-control") for b in acc):
        F.add("L2-15", "LOW", "No storm-control on access ports", [(b.lineno, b.header) for b in acc[:3]],
              "storm-control broadcast level 1.00\nstorm-control multicast level 5.00\nstorm-control action trap")

    snoop = cfg.g(r"^ip dhcp snooping$")
    snoop_vl = cfg.g(r"^ip dhcp snooping vlan")
    if acc and not snoop:
        F.add("L2-16", "MEDIUM", "DHCP snooping not enabled (rogue DHCP / MITM)", "No 'ip dhcp snooping'",
              "ip dhcp snooping vlan <user-vlans>\nip dhcp snooping\ninterface <uplink>\n ip dhcp snooping trust")
    if snoop and not snoop_vl:
        F.add("CORR-04", "MEDIUM", "DHCP snooping enabled globally but no VLANs selected (no protection)", snoop,
              "ip dhcp snooping vlan <user-vlans>")
    if snoop and snoop_vl:
        trusted = [b for b in all_if if b.has(r"^ip dhcp snooping trust")]
        has_local_l3 = any(classify(b) == "svi" and b.has(r"^ip helper-address") for b in all_if)
        if not trusted and not has_local_l3:
            F.add("CORR-05", "HIGH", "DHCP snooping active but no trusted ports (legitimate DHCP replies dropped)",
                  snoop_vl,
                  "interface <uplink toward DHCP server/relay>\n ip dhcp snooping trust",
                  note="With no trusted interface every OFFER/ACK from the real server is dropped, so clients on the "
                       "snooped VLANs stop getting leases as their old ones expire.")
        elif not trusted and has_local_l3:
            F.add("CORR-05", "LOW", "DHCP snooping with no trusted ports (OK only if this switch is the relay)",
                  snoop_vl, "Trust any downlink trunk to switches that also snoop, or replies won't reach them.",
                  confidence="verify")
        if not cfg.g(r"^no ip dhcp snooping information option") and trusted:
            F.add("CORR-07", "INFO", "Snooping inserts Option 82; non-relay upstream may drop requests", snoop_vl,
                  "no ip dhcp snooping information option   ! if upstream relay rejects option 82",
                  confidence="verify")
    dai = cfg.g(r"^ip arp inspection vlan")
    if acc and not dai:
        F.add("L2-17", "MEDIUM", "Dynamic ARP Inspection not enabled (ARP spoofing / MITM)",
              "No 'ip arp inspection vlan'",
              "ip arp inspection vlan <user-vlans>   ! needs DHCP snooping; 'ip arp inspection trust' on uplinks",
              confidence="verify")
    if dai and not snoop:
        F.add("CORR-08", "HIGH", "DAI enabled without DHCP snooping (dynamic hosts' ARP dropped)", dai,
              "Enable DHCP snooping on the same VLANs, or add ARP ACLs for static hosts.")
    if dai and not [b for b in all_if if b.has(r"^ip arp inspection trust")]:
        F.add("CORR-09", "HIGH", "DAI enabled but no trusted interfaces (uplink ARP dropped)", dai,
              "interface <uplink>\n ip arp inspection trust")
    if cfg.g(r"^ipv6 unicast-routing") or any(b.has(r"^ipv6 (address|enable)") for b in all_if):
        if not cfg.g(r"^ipv6 nd raguard policy|^device-tracking policy"):
            F.add("L2-18", "LOW", "IPv6 present without RA Guard / first-hop security", "No RA guard policy",
                  "ipv6 nd raguard policy HOST\n device-role host\n(attach on access ports)", confidence="verify")

    # ---------------- Layer 3
    l3 = [b for b in live if classify(b) in ("svi", "routed") and b.has(r"^ip address \d")]
    pa = [b for b in l3 if not b.has(r"^no ip proxy-arp")]
    if pa:
        F.add("L3-01", "LOW", "Proxy ARP enabled on L3 interfaces", [(b.lineno, b.header) for b in pa], "no ip proxy-arp")
    rd = [b for b in l3 if not b.has(r"^no ip redirects")]
    if rd:
        F.add("L3-02", "INFO", "ICMP redirects/unreachables enabled on L3 interfaces",
              [(b.lineno, b.header) for b in rd], "no ip redirects\nno ip unreachables")
    dbc = [b for b in l3 if b.has(r"^ip directed-broadcast")]
    if dbc:
        F.add("L3-03", "HIGH", "IP directed-broadcast enabled (smurf amplification)",
              [(b.lineno, b.header) for b in dbc], "no ip directed-broadcast")
    for b in all_if:
        for n, c in b.find(r"^ip access-group \S+ (in|out)"):
            a = c.split()[2]
            if a not in acls:
                F.add("CORR-10", "HIGH", f"{ifname(b)}: access-group '{a}' is not defined (interface is unfiltered)",
                      [(n, c)], f"Define ACL {a}. IOS treats a missing ACL as permit-all on interfaces.")
    hsrp = [(n, f"{ifname(b)}: {c}") for b in all_if for n, c in b.find(r"^standby (\d+ )?ip")]
    if hsrp and not any(b.has(r"^standby .*authentication") for b in all_if):
        F.add("L3-04", "MEDIUM", "HSRP without MD5 authentication (gateway hijack)", hsrp,
              "standby <grp> authentication md5 key-string <key>",
              note="Any host on the VLAN can send HSRP hellos with a higher priority and become the default gateway (MITM).")
    for b in cfg.blocks_matching(r"^router ospf"):
        if not b.has(r"area \S+ authentication") and \
                not any(i.has(r"^ip ospf (authentication|message-digest-key)") for i in all_if):
            F.add("L3-05", "MEDIUM", f"{b.header}: OSPF without neighbor authentication", [(b.lineno, b.header)],
                  "area 0 authentication message-digest + 'ip ospf message-digest-key 1 md5 <key>' "
                  "(or key chains with HMAC-SHA)")
        if not b.has(r"^passive-interface default"):
            F.add("L3-06", "MEDIUM" if l3 and any(classify(x) == "svi" for x in l3) else "LOW",
                  f"{b.header}: no 'passive-interface default' (OSPF hellos on user VLANs)", [(b.lineno, b.header)],
                  "passive-interface default\nno passive-interface <uplinks>",
                  note="Combined with no authentication, a host on a user VLAN can form an adjacency and inject routes.")
    for b in cfg.blocks_matching(r"^router eigrp"):
        if not b.has(r"authentication") and not any(i.has(r"^ip authentication mode eigrp") for i in all_if):
            F.add("L3-05", "MEDIUM", f"{b.header}: EIGRP without authentication", [(b.lineno, b.header)],
                  "Named mode: af-interface default / authentication mode hmac-sha-256 <key>")
    for b in cfg.blocks_matching(r"^router bgp"):
        nbrs = {c.split()[1] for _, c in b.find(r"^neighbor \S+ remote-as")}
        pw = {c.split()[1] for _, c in b.find(r"^neighbor \S+ password")}
        if nbrs - pw:
            F.add("L3-07", "LOW", f"{b.header}: BGP neighbors without TCP-MD5/AO", [(b.lineno, ", ".join(sorted(nbrs - pw)))],
                  "neighbor <ip> password <key>", confidence="verify")
    if cfg.g(r"^ip routing") and cfg.g(r"^ip default-gateway"):
        F.add("CORR-11", "LOW", "'ip default-gateway' set while 'ip routing' is on (ignored)",
              cfg.g(r"^ip default-gateway"), "Use 'ip route 0.0.0.0 0.0.0.0 <next-hop>'.")
    seen = {}
    for b in all_if:
        for n, c in b.find(r"^ip address \d+\.\d+\.\d+\.\d+ "):
            seen.setdefault(c.split()[2], []).append((n, f"{ifname(b)}: {c}"))
    for ip, lst in seen.items():
        if len(lst) > 1:
            F.add("CORR-12", "MEDIUM", f"Duplicate IP {ip} on multiple interfaces", lst, "Correct addressing.")
    defined_vlans = set()
    for _, l in cfg.g(r"^vlan [\d,\-]+$"):
        for part in l.split()[1].split(","):
            if "-" in part:
                a, z = part.split("-")
                defined_vlans.update(range(int(a), int(z) + 1))
            else:
                defined_vlans.add(int(part))
    if defined_vlans:
        missing = []
        for b in acc + [b for b in all_if if b.has(r"^switchport voice vlan \d")]:
            for pat in (r"^switchport access vlan (\d+)", r"^switchport voice vlan (\d+)"):
                m = b.first(pat)
                if m and int(m.group(1)) not in defined_vlans and m.group(1) != "1":
                    missing.append((b.lineno, f"{ifname(b)} -> vlan {m.group(1)}"))
        if missing:
            F.add("CORR-13", "MEDIUM", "Ports assigned to VLANs not defined on the switch (port inactive / no forwarding)",
                  sorted(set(missing)), "vlan <id>\n name <name>", confidence="likely",
                  note="Confirm with 'show vlan brief' / 'show interfaces <if> switchport' (look for 'inactive').")
        for b in trunks_report:
            m = b.first(r"^switchport trunk native vlan (\d+)")
            if m and int(m.group(1)) not in defined_vlans:
                F.add("CORR-14", "LOW", f"{ifname(b)}: native VLAN {m.group(1)} not defined", [(b.lineno, b.header)],
                      f"vlan {m.group(1)}", confidence="likely")

    seen_keys = set()
    uniq = []
    for i in F.items:
        k = (i["id"], i["title"])
        if k in seen_keys:
            continue
        seen_keys.add(k)
        uniq.append(i)
    uniq.sort(key=lambda x: (SEV_ORDER[x["severity"]], x["id"]))
    return uniq


# --------------------------------------------------------------------------- output
def inventory(cfg):
    kinds = {}
    for b in cfg.interfaces:
        k = classify(b) + (" (shutdown)" if is_shut(b) else "")
        kinds[k] = kinds.get(k, 0) + 1
    return OrderedDict(
        hostname=cfg.hostname, version=cfg.version, file=cfg.name, interfaces=kinds,
        l3_routing=bool(cfg.g(r"^ip routing")), aaa=bool(cfg.g(r"^aaa new-model")),
        vlans_in_config=len(cfg.g(r"^vlan \d")),
    )


def to_markdown(cfg, items):
    inv = inventory(cfg)
    counts = {}
    for i in items:
        counts[i["severity"]] = counts.get(i["severity"], 0) + 1
    out = [f"## {inv['hostname']}  ({inv['file']})",
           f"- Version line: `{inv['version']}` | ip routing: {inv['l3_routing']} | aaa new-model: {inv['aaa']} "
           f"| VLANs defined in config: {inv['vlans_in_config']}",
           "- Interfaces by role: " + ", ".join(f"{k}={v}" for k, v in sorted(inv["interfaces"].items())),
           "- Counts: " + ", ".join(f"{s} {counts.get(s, 0)}" for s in SEV_ORDER),
           ""]
    for i in items:
        conf = "" if i["confidence"] == "confirmed" else f"  [{i['confidence']}]"
        out.append(f"### [{i['severity']}] {i['id']}: {i['title']}{conf}")
        for e in i["evidence"]:
            out.append(f"    {e}")
        if i.get("note"):
            out.append(f"- Note: {i['note']}")
        out.append("- Fix:\n```\n" + i["fix"] + "\n```\n")
    return "\n".join(out)


def main(argv):
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    as_json = "--json" in argv
    show = "--show-secrets" in argv
    results = []
    for path in paths:
        with open(path, encoding="utf-8", errors="replace") as fh:
            cfg = Config(fh.read(), path)
        items = run_checks(cfg, show)
        if as_json:
            results.append({"inventory": inventory(cfg), "findings": items})
        else:
            print(to_markdown(cfg, items))
    if as_json:
        print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
