# ibx-nios-sdk Phase 4: Security Cluster Implementation Plan

**Goal:** Implement 5 security-related domains: `rpz` (17 objects), `threatprotection` (8), `threatinsight` (4), `security` (21), `acl` (1). Total: 51 objects.

**Precedent:** DNS / IPAM / DHCP / Grid domains already implemented at `src/ibx_nios_sdk/`. Follow the same per-domain pattern wholesale.

**Swaggers:** Each sub-domain gets its own `schemas/v2.14/<domain>.json` snapshot.

For each sub-domain: scaffold → per-object-batch commits → final commit. Each sub-domain produces ~3–5 commits.

---

## Sub-domain 1: `rpz` (17 objects)

Response-policy-zone records. Nearly identical in shape to DNS records but for RPZ zones.

**Objects:**
- `Allrpzrecords` (read-only aggregate)
- `RecordRpzA`, `RecordRpzAaaa`, `RecordRpzCname`, `RecordRpzHttps`, `RecordRpzMx`, `RecordRpzNaptr`, `RecordRpzPtr`, `RecordRpzSrv`, `RecordRpzSvcb`, `RecordRpzTxt`
- Address-based RPZ records: `RecordRpzAIpaddress`, `RecordRpzAaaaIpaddress`
- CNAME policy variants: `RecordRpzCnameIpaddress`, `RecordRpzCnameIpaddressdn`, `RecordRpzCnameClientipaddress`, `RecordRpzCnameClientipaddressdn`

**Commits (3 expected):**
1. `feat(rpz): scaffold rpz package and wire RpzService into NiosClient`
2. `feat(rpz): add standard RPZ record types (a, aaaa, cname, https, mx, naptr, ptr, srv, svcb, txt)`
3. `feat(rpz): add RPZ address and cname-ipaddress policy records + allrpzrecords aggregate`

---

## Sub-domain 2: `threatprotection` (8 objects)

**Objects:** `ThreatprotectionGridRule`, `ThreatprotectionProfile`, `ThreatprotectionProfileRule`, `ThreatprotectionRule`, `ThreatprotectionRulecategory`, `ThreatprotectionRuleset`, `ThreatprotectionRuletemplate`, `ThreatprotectionStatistics`

**WAPI types:**
- `grid:threatprotection:rule` (GridRule)
- `threatprotection:profile`
- `threatprotection:profile:rule`
- `threatprotection:rule`
- `threatprotection:rulecategory`
- `threatprotection:ruleset`
- `threatprotection:ruletemplate`
- `threatprotection:statistics`

`ThreatprotectionStatistics` is read-only.

**Commits (2 expected):**
1. `feat(threatprotection): scaffold threatprotection package and wire into NiosClient`
2. `feat(threatprotection): add 8 threat protection resources`

---

## Sub-domain 3: `threatinsight` (4 objects)

**Objects:** `ThreatinsightAllowlist`, `ThreatinsightCloudclient`, `ThreatinsightInsightAllowlist`, `ThreatinsightModuleset`

**WAPI types:**
- `threatinsight:allowlist`
- `threatinsight:cloudclient`
- `threatinsight:insightallowlist`
- `threatinsight:moduleset`

**Commits (2 expected):**
1. `feat(threatinsight): scaffold threatinsight package and wire into NiosClient`
2. `feat(threatinsight): add 4 threat insight resources`

---

## Sub-domain 4: `security` (21 objects)

**Objects grouped:**

- **Users + roles (6):** `Admingroup`, `Adminrole`, `Adminuser`, `Permission`, `Userprofile`, `Authpolicy`
- **Auth services (8):** `Approvalworkflow`, `Cacertificate`, `CertificateAuthservice`, `RadiusAuthservice`, `TacacsplusAuthservice`, `LdapAuthService`, `SamlAuthservice`, `LocaluserAuthservice`
- **Other auth (3):** `AdAuthService`, `Snmpuser`, `Ftpuser`
- **Network users (1):** `Networkuser`
- **HSM (3):** `HsmAllgroups`, `HsmEntrustnshieldgroup`, `HsmThaleslunagroup`

**Commits (4–6 expected):**
1. `feat(security): scaffold security package and wire into NiosClient`
2. `feat(security): add admin users, groups, roles, permissions, userprofile, authpolicy`
3. `feat(security): add approvalworkflow + auth services (ca cert, radius, tacacs, ldap, saml, local, cert)`
4. `feat(security): add AD auth + SNMP users + FTP users + network users`
5. `feat(security): add HSM group resources`

---

## Sub-domain 5: `acl` (1 object)

**Object:** `Namedacl`.

One object, one commit with scaffolding + the resource:
- `feat(acl): scaffold acl package and add Namedacl resource`

---

## Cross-cutting conventions (unchanged from prior phases)

- Every resource: model + resource + test + DomainService wiring + dns/ipam/dhcp-style file layout.
- 6-scenario tests minimum per object (list, get, find_one, create, update_strips_readonly, delete).
- Use `ExtAttrValue` from `ibx_nios_sdk._common.models` for extattrs.
- `_<Domain>Nested` base in each `<domain>/models/_shared.py`.
- Python keyword collisions: `type_` with `Field(alias="type")`. `READONLY_FIELDS` uses Python attribute names.
- Deeply nested / function-schema fields can be `dict[str, Any] | None` with NOTES.md entries.
- Commit per batch, pytest + mypy + ruff + ruff format all clean before each commit.
- Final commit per sub-domain: `feat(<domain>): Phase 4 <domain> complete - all N <domain> object types covered`.

---

## Verification Checklist

- [ ] All 5 sub-domains scaffolded with `<Domain>Service` cached on `NiosClient`.
- [ ] Every swagger tag in each sub-domain has a corresponding resource class.
- [ ] Full pytest suite passes.
- [ ] mypy strict, ruff check, ruff format --check all clean.
- [ ] Five examples (or one consolidated example) demonstrate each sub-domain.
