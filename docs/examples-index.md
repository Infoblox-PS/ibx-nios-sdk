# Example Scripts

22 Click-based workflow examples live under `docs/examples/`.  Each script is a
standalone Python file with a `@click.group()` interface - no installation required
beyond the SDK itself.

Clone the repo and run any script directly:

```bash
python docs/examples/<script>.py --help
python docs/examples/<script>.py <subcommand> --help
```

All scripts share the same connection options (`--grid-url`, `--username`,
`--password`, `--wapi-ver`, `--verify/--no-verify`) and authenticate via
NIOS session cookies.

List commands on 8 scripts support `--json` for scripting - see each script's `--help`.

## Script index

| Domain | Script | Source |
|---|---|---|
| DNS | `manage_dns_zones.py` | [examples/manage_dns_zones.py](examples/manage_dns_zones.py) |
| DNS | `manage_dns_records.py` | [examples/manage_dns_records.py](examples/manage_dns_records.py) |
| DNS | `manage_dns_views.py` | [examples/manage_dns_views.py](examples/manage_dns_views.py) |
| DNS | `manage_rpz.py` | [examples/manage_rpz.py](examples/manage_rpz.py) |
| IPAM/DHCP | `manage_networks.py` | [examples/manage_networks.py](examples/manage_networks.py) |
| IPAM/DHCP | `manage_dhcp_ranges.py` | [examples/manage_dhcp_ranges.py](examples/manage_dhcp_ranges.py) |
| IPAM/DHCP | `manage_dhcp_leases.py` | [examples/manage_dhcp_leases.py](examples/manage_dhcp_leases.py) |
| IPAM/DHCP | `manage_next_available_ip.py` | [examples/manage_next_available_ip.py](examples/manage_next_available_ip.py) |
| DTC | `manage_dtc.py` | [examples/manage_dtc.py](examples/manage_dtc.py) |
| DTC | `manage_dtc_pools.py` | [examples/manage_dtc_pools.py](examples/manage_dtc_pools.py) |
| DTC | `manage_dtc_servers.py` | [examples/manage_dtc_servers.py](examples/manage_dtc_servers.py) |
| DTC | `manage_dtc_full.py` | [examples/manage_dtc_full.py](examples/manage_dtc_full.py) |
| Grid | `manage_grid.py` | [examples/manage_grid.py](examples/manage_grid.py) |
| Grid | `manage_members.py` | [examples/manage_members.py](examples/manage_members.py) |
| Grid | `manage_fileop.py` | [examples/manage_fileop.py](examples/manage_fileop.py) |
| Security | `manage_admin_users.py` | [examples/manage_admin_users.py](examples/manage_admin_users.py) |
| Security | `manage_auth_services.py` | [examples/manage_auth_services.py](examples/manage_auth_services.py) |
| Threat | `manage_threat_protection.py` | [examples/manage_threat_protection.py](examples/manage_threat_protection.py) |
| Cloud / Discovery | `manage_cloud.py` | [examples/manage_cloud.py](examples/manage_cloud.py) |
| Cloud / Discovery | `manage_discovery.py` | [examples/manage_discovery.py](examples/manage_discovery.py) |
| MS Server | `manage_ms_server.py` | [examples/manage_ms_server.py](examples/manage_ms_server.py) |
| Notification | `manage_notifications.py` | [examples/manage_notifications.py](examples/manage_notifications.py) |

---

## DNS

### `manage_dns_zones.py`

Manage NIOS authoritative DNS zones - list, inspect, create, update, delete, copy
records between zones, and lock/unlock zones.

**Subcommands:** `list`, `get`, `create`, `update`, `delete`, `copy-records`, `lock-unlock`

```bash
python docs/examples/manage_dns_zones.py list --fqdn-like example
python docs/examples/manage_dns_zones.py create --fqdn internal.example.com
```

---

### `manage_dns_records.py`

Create and list individual DNS resource records (A, AAAA, CNAME, MX, TXT, Host) and
delete records by WAPI reference.

**Subcommands:** `list-a`, `create-a`, `create-aaaa`, `create-cname`, `create-mx`,
`create-txt`, `create-host`, `delete`

```bash
python docs/examples/manage_dns_records.py list-a --zone example.com
python docs/examples/manage_dns_records.py create-a --name web.example.com --ipv4addr 10.0.0.1
```

---

### `manage_dns_views.py`

List, inspect, create, update, and delete NIOS DNS views.

**Subcommands:** `list`, `get`, `create`, `update`, `delete`

```bash
python docs/examples/manage_dns_views.py list --name-like internal
python docs/examples/manage_dns_views.py create --name internal-view
```

---

## IPAM

### `manage_networks.py`

Manage IPv4 and IPv6 networks and network containers - list, create, delete across
default and named network views.

**Subcommands:** `list-v4`, `list-v6`, `list-containers-v4`, `list-containers-v6`,
`create-v4`, `create-v6`, `create-container-v4`, `create-container-v6`, `delete`

```bash
python docs/examples/manage_networks.py list-v4 --network 10.0.0.0/8
python docs/examples/manage_networks.py create-v4 --network 192.168.100.0/24 --comment "Lab subnet"
```

---

### `manage_next_available_ip.py`

Allocate the next available IP from a network, the next available network from a
container, or atomically create an A record using the next free IP.

**Subcommands:** `next-ip`, `next-network`, `allocate-host`

```bash
python docs/examples/manage_next_available_ip.py next-ip network/ZG5z:10.0.0.0/24/default --num 3
python docs/examples/manage_next_available_ip.py allocate-host --network-ref <ref> --hostname web01.example.com
```

---

## DHCP

### `manage_dhcp_ranges.py`

Manage DHCP ranges and fixed-address reservations for both IPv4 and IPv6.

**Subcommands:** `list-ranges`, `create-range`, `range-next-ip`, `list-fixed`,
`create-fixed`, `delete-fixed`, `list-ranges-v6`, `create-range-v6`,
`list-fixed-v6`, `create-fixed-v6`, `delete-fixed-v6`

```bash
python docs/examples/manage_dhcp_ranges.py list-ranges --network 10.0.0.0/24
python docs/examples/manage_dhcp_ranges.py create-range --network 10.0.0.0/24 \
    --start-addr 10.0.0.100 --end-addr 10.0.0.200
```

---

### `manage_dhcp_leases.py`

List and inspect active DHCP leases with filtering by network, binding state,
IP address, and hostname; print a per-network utilisation summary.

**Subcommands:** `list`, `get`, `summary`

```bash
python docs/examples/manage_dhcp_leases.py list --network 10.0.0.0/24 --binding-state ACTIVE
python docs/examples/manage_dhcp_leases.py summary --network 10.0.0.0/24
```

---

## Grid & Members

### `manage_grid.py`

Inspect Grid settings, list Grids, manage extensible attribute definitions, and
trigger grid-wide service restarts.

**Subcommands:** `show-grid`, `list-grids`, `list-ea-defs`, `create-ea-def`,
`delete-ea-def`, `restart-grid-services`

```bash
python docs/examples/manage_grid.py show-grid
python docs/examples/manage_grid.py restart-grid-services --services DNS --services DHCP
```

---

### `manage_members.py`

List Grid members, fetch a specific member by name, restart services on individual
members, and check member-level restart status.

**Subcommands:** `list`, `get`, `restart-services`, `list-restart-status`

```bash
python docs/examples/manage_members.py list --platform VNIOS
python docs/examples/manage_members.py restart-services ns1.example.com --services DNS
```

---

## DTC (DNS Traffic Control)

### `manage_dtc_servers.py`

Manage DTC server objects - the individual back-end hosts that pools draw from.

**Subcommands:** `list`, `get`, `create`, `update`, `delete`

```bash
python docs/examples/manage_dtc_servers.py list --name-like web
python docs/examples/manage_dtc_servers.py create --name web01 --host 10.0.0.10
```

---

### `manage_dtc_pools.py`

Manage DTC pools - groups of DTC servers with associated health monitors and load
balancing policy.

**Subcommands:** `list`, `get`, `create`, `add-member`, `remove-member`, `delete`

```bash
python docs/examples/manage_dtc_pools.py list
python docs/examples/manage_dtc_pools.py create --name web-pool --lb-method ROUND_ROBIN
```

---

### `manage_dtc.py`

Manage DTC health monitors (HTTP, TCP, ICMP), LBDN objects, and topology rules.

**Subgroups / subcommands:**
`monitors list-http`, `monitors list-tcp`, `monitors list-icmp`,
`monitors create-http`, `monitors create-tcp`, `monitors create-icmp`,
`monitors delete-monitor`,
`lbdn list`, `lbdn get`, `lbdn create`, `lbdn delete`,
`topology list`, `topology create`, `topology add-rule`, `topology delete`

```bash
python docs/examples/manage_dtc.py monitors list-http
python docs/examples/manage_dtc.py lbdn create --name web-lbdn --lb-method TOPOLOGY
```

---

### `manage_dtc_full.py`

Flagship end-to-end DTC workflow - deploy a complete multi-pool DTC setup from a
single command, tear it down, inspect status and health, or migrate between load
balancing methods.

**Subcommands:** `deploy`, `teardown`, `status`, `health`, `migrate`

```bash
# Deploy a full DTC stack (monitors + servers + pools + LBDN)
python docs/examples/manage_dtc_full.py deploy \
    --lbdn-name web.example.com \
    --server-hosts 10.0.0.10,10.0.0.11 \
    --lb-method ROUND_ROBIN

# Tear it all down
python docs/examples/manage_dtc_full.py teardown --lbdn-name web.example.com

# Show current status
python docs/examples/manage_dtc_full.py status --lbdn-name web.example.com
```

---

## Security

### `manage_admin_users.py`

Manage NIOS admin users, groups, roles, permissions, and the authentication policy
(local vs LDAP/RADIUS ordering).

**Subcommands:** `list-users`, `create-user`, `list-groups`, `create-group`,
`list-roles`, `list-permissions`, `get-authpolicy`, `update-authpolicy`

```bash
python docs/examples/manage_admin_users.py list-users --name-like ops
python docs/examples/manage_admin_users.py create-user --username noc --groups "Read-Only Users"
```

---

### `manage_auth_services.py`

Configure NIOS external authentication services - list existing LDAP/RADIUS services,
add new services, delete services, and manage CA certificates.

**Subcommands:** `list-services`, `add-ldap`, `add-radius`, `delete-service`,
`list-ca-certs`, `show-cert`

```bash
python docs/examples/manage_auth_services.py list-services
python docs/examples/manage_auth_services.py add-ldap \
    --name corporate-ldap --ldap-server ldap.corp.example.com \
    --search-base "dc=corp,dc=example,dc=com" --bind-dn "cn=svc,dc=corp,dc=example,dc=com"
```

---

## RPZ

### `manage_rpz.py`

Create and manage Response Policy Zones (RPZ) - list zones, create LOCAL or
GIVEN_IP policy zones, manage A and CNAME block records, and create IP block records.

**Subcommands:** `list-zones`, `create-zone`, `delete-zone`, `list-a-records`,
`create-a-record`, `create-cname-block`, `create-ip-block`, `delete-record`

```bash
python docs/examples/manage_rpz.py list-zones
python docs/examples/manage_rpz.py create-zone --fqdn malware.rpz.example.com --view default
```

---

## Discovery

### `manage_discovery.py`

Explore network discovery results - list discovered devices, device components and
interfaces; manage credential groups; read diagnostic tasks; and manage vDiscovery
tasks for virtual infrastructure.

**Subcommands:** `list-devices`, `get-device`, `list-device-components`,
`list-device-interfaces`, `list-credential-groups`, `create-credential-group`,
`list-diagnostic-tasks`, `show-diagnostic-task`, `list-vdiscovery-tasks`,
`create-vdiscovery-task`

```bash
python docs/examples/manage_discovery.py list-devices --type SWITCH
python docs/examples/manage_discovery.py list-device-interfaces --device-ref <ref>
```

---

## Cloud

### `manage_cloud.py`

Manage Cloud Network Automation integration for AWS, Azure, and GCP - task groups and
cloud users per provider, plus multi-region discovery configuration.

**Subgroups / subcommands:**
`aws list-task-groups`, `aws create-task-group`, `aws delete-task-group`, `aws list-users`, `aws create-user`;
same pattern for `azure` and `gcp`;
`list-multiregions`

```bash
python docs/examples/manage_cloud.py aws list-task-groups
python docs/examples/manage_cloud.py azure create-task-group \
    --name prod-azure --account-id <subscription-id>
```

---

## Notifications

### `manage_notifications.py`

Configure outbound notification rules, endpoints (webhook URLs), and templates for
event-driven integrations (Slack, ServiceNow, custom webhooks).

**Subgroups / subcommands:**
`endpoints list`, `endpoints create`, `endpoints delete`,
`templates list`, `templates get`,
`rules list`, `rules create`, `rules delete`

```bash
python docs/examples/manage_notifications.py endpoints list
python docs/examples/manage_notifications.py endpoints create \
    --name slack-ops --uri https://hooks.slack.com/services/... --auth-type NONE
```

---

## Threat Protection

### `manage_threat_protection.py`

Manage Advanced DNS Protection (ADP) profiles, rules, and Threat Intelligence (TI)
allowlists, modulesets, and cloud client settings.

**Subgroups / subcommands:**
`tp list-profiles`, `tp list-rules`, `tp list-rulesets`, `tp list-ruletemplates`,
`tp create-profile`, `tp delete-profile`, `tp stats`;
`ti list-allowlists`, `ti create-allowlist`, `ti delete-allowlist`,
`ti list-modulesets`, `ti show-cloudclient`, `ti update-cloudclient`

```bash
python docs/examples/manage_threat_protection.py tp list-profiles
python docs/examples/manage_threat_protection.py ti show-cloudclient
```

---

## Microsoft Server Integration

### `manage_ms_server.py`

Manage Microsoft server integrations - list, add, and remove Microsoft DNS/DHCP
servers synced to NIOS; inspect DNS and DHCP scopes on those servers; list AD sites
and domains.

**Subcommands:** `list-servers`, `get`, `add-server`, `remove-server`,
`list-dns-on`, `list-dhcp-on`, `list-adsites`, `list-domains`

```bash
python docs/examples/manage_ms_server.py list-servers --domain corp.example.com
python docs/examples/manage_ms_server.py list-dns-on <server_ref>
```

---

## Fileop Operations

### `manage_fileop.py`

Convenience wrapper around several NIOS fileop operations - CSV export, CSV import,
support bundle download, global object search, member log download, and certificate
download - from a single grouped script.

**Subcommands:** `csv-export`, `csv-import`, `support-bundle`, `search`,
`get-log`, `get-cert`

```bash
python docs/examples/manage_fileop.py csv-export --object network --output networks.csv
python docs/examples/manage_fileop.py support-bundle --member ns1.example.com \
    --output ns1_bundle.tar.gz
```
