# Security

The `security` domain covers **27 resources**: admin users, groups, roles, and permissions;
authentication policy; approval workflows; authentication services (CA cert, RADIUS, TACACS+,
LDAP, SAML, local users, certificate-based); Active Directory auth; RADIUS users and NAS
clients; SNMP/FTP/network users; parental-control subscribers, policies and AVPs; and HSM
groups.

Access via `client.security`.

---

## Admin users

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient() as client:
        # List all admin users
        async for user in client.security.adminuser.list():
            print(user.name, user.status)

        # Create a read-only admin user
        user = await client.security.adminuser.create({
            "name": "readonly-ops",
            "password": "S3cur3P@ss!",
            "status": "ENABLED",
            "admin_groups": ["readonly-group"],
            "comment": "Ops read-only account",
        })
        print(user._ref)

        # Disable an account
        await client.security.adminuser.update(user._ref, {"status": "DISABLED"})

asyncio.run(main())
```

---

## Admin groups

Admin groups control what operations users can perform.

```python
async with NiosClient() as client:
    # List all groups
    groups = await client.security.admingroup.list().all()
    for g in groups:
        print(g.name, g.comment)

    # Create a custom group
    grp = await client.security.admingroup.create({
        "name": "dns-admins",
        "comment": "DNS administration team",
        "superuser": False,
        "roles": ["dns-role"],
    })
```

---

## Admin roles

Roles aggregate permissions into reusable policies.

```python
async with NiosClient() as client:
    roles = await client.security.adminrole.list().all()
    for r in roles:
        print(r.name, r.comment)

    new_role = await client.security.adminrole.create({
        "name": "dns-readonly",
        "comment": "Read-only DNS access",
    })
```

---

## Permissions

Permissions map a role to a specific WAPI resource type and access level.

```python
async with NiosClient() as client:
    # List permissions for a role
    perms = await client.security.permission.list(role="dns-readonly").all()
    for p in perms:
        print(p.resource_type, p.permission)

    # Grant read access to zone_auth
    perm = await client.security.permission.create({
        "role": "dns-readonly",
        "resource_type": "zone_auth",
        "permission": "READ",
    })
```

---

## Authentication policy

The auth policy determines the order in which auth services are tried.

```python
async with NiosClient() as client:
    # Get the single auth policy
    policies = await client.security.authpolicy.list().all()
    policy = policies[0]

    # Update auth service order
    await client.security.authpolicy.update(
        policy._ref,
        {"auth_services": ["local_authservice", "radius_authservice"]},
    )
```

---

## Authentication services

| Resource | Auth service type |
|---|---|
| `localuser_authservice` | Local NIOS user database |
| `radius_authservice` | RADIUS server |
| `tacacsplus_authservice` | TACACS+ server |
| `ldap_auth_service` | LDAP / Active Directory |
| `saml_authservice` | SAML 2.0 IdP |
| `certificate_authservice` | Certificate-based auth |
| `cacertificate` | CA certificate store |
| `ad_auth_service` | Active Directory auth service |

```python
async with NiosClient() as client:
    # RADIUS auth service
    radius = await client.security.radius_authservice.create({
        "name": "corp-radius",
        "auth_servers": [
            {
                "address": "10.0.0.50",
                "shared_secret": "r@d1us_secret",
                "port": 1812,
            }
        ],
        "comment": "Corporate RADIUS",
    })

    # LDAP auth service
    ldap = await client.security.ldap_auth_service.create({
        "name": "corp-ad",
        "ldap_user_attribute": "sAMAccountName",
        "servers": [{"address": "dc1.corp.example.com", "port": 389}],
        "comment": "Active Directory LDAP",
    })
```

---

## Approval workflows

Approval workflows require a second admin to approve changes before they are applied.

```python
async with NiosClient() as client:
    # List workflows
    workflows = await client.security.approvalworkflow.list().all()
    for wf in workflows:
        print(wf.approver_type, wf.approved_type)

    # Create a workflow requiring approval for zone_auth changes
    wf = await client.security.approvalworkflow.create({
        "approved_type": "zone_auth",
        "approver_type": "GROUP",
        "approver": "dns-approvers",
        "rascal_task_id": "auto",
    })
```

---

## SNMP, FTP, and network users

```python
async with NiosClient() as client:
    # SNMP users (SNMPv3)
    snmp_users = await client.security.snmpuser.list().all()

    # FTP users (for file distribution)
    ftp_users = await client.security.ftpuser.list().all()

    # Network users (DHCP lease-based auth)
    net_users = await client.security.networkuser.list().all()

    # User profile (current session's profile)
    profile = await client.security.userprofile.list().all()
```

---

## Parental control

Parental control applies per-subscriber DNS policies - useful for ISPs and managed
service providers. Five resources cooperate to express a policy.

| Resource | Purpose |
|---|---|
| `parentalcontrol_subscribersite` | Site-level configuration (per deployment) |
| `parentalcontrol_subscriber` | Subscriber schema definitions |
| `parentalcontrol_subscriberrecord` | Individual subscriber → policy bindings |
| `parentalcontrol_blockingpolicy` | Named blocking policies referenced by records |
| `parentalcontrol_avp` | RADIUS AVPs used to correlate sessions to subscribers |

```python
async with NiosClient() as client:
    # Blocking policies available to subscribers
    policies = await client.security.parentalcontrol_blockingpolicy.list().all()
    for p in policies:
        print(p.name, p.value)

    # Subscriber records (per-subscriber policy bindings)
    async for rec in client.security.parentalcontrol_subscriberrecord.list():
        print(rec.subscriber_id, rec.parental_control_policy)

    # AVP definitions (RADIUS attribute-value pair mappings)
    avps = await client.security.parentalcontrol_avp.list().all()

    # Site and subscriber schema singletons
    sites = await client.security.parentalcontrol_subscribersite.list().all()
    subscribers = await client.security.parentalcontrol_subscriber.list().all()
```

!!! note
    Parental-control objects are NIOS 8.x+ features and require the appropriate license.
    Expect 404s from the WAPI if the feature is not enabled on your grid.

---

## HSM groups

Hardware Security Module groups store DNSSEC private keys off-appliance.

```python
async with NiosClient() as client:
    # All HSM groups (any vendor)
    all_hsm = await client.security.hsm_allgroups.list().all()

    # Entrust nShield groups
    entrust = await client.security.hsm_entrustnshieldgroup.list().all()

    # Thales Luna groups
    thales = await client.security.hsm_thaleslunagroup.list().all()
```
