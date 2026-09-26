# Security Domain - Implementation Notes

## WAPI Type Verification (swagger ground truth)

All WAPI types verified against `/schemas/v2.14/security.json` paths. The plan's WAPI types
were accurate; no discrepancies found.

| Class | WAPI Type | Path verified |
|---|---|---|
| Admingroup | `admingroup` | `/admingroup` |
| Adminrole | `adminrole` | `/adminrole` |
| Adminuser | `adminuser` | `/adminuser` |
| Permission | `permission` | `/permission` |
| Userprofile | `userprofile` | `/userprofile` |
| Authpolicy | `authpolicy` | `/authpolicy` |
| Approvalworkflow | `approvalworkflow` | `/approvalworkflow` |
| Cacertificate | `cacertificate` | `/cacertificate` |
| CertificateAuthservice | `certificate:authservice` | `/certificate:authservice` |
| RadiusAuthservice | `radius:authservice` | `/radius:authservice` |
| TacacsplusAuthservice | `tacacsplus:authservice` | `/tacacsplus:authservice` |
| LdapAuthService | `ldap_auth_service` | `/ldap_auth_service` |
| SamlAuthservice | `saml:authservice` | `/saml:authservice` |
| LocaluserAuthservice | `localuser:authservice` | `/localuser:authservice` |
| AdAuthService | `ad_auth_service` | `/ad_auth_service` |
| Snmpuser | `snmpuser` | `/snmpuser` |
| Ftpuser | `ftpuser` | `/ftpuser` |
| Networkuser | `networkuser` | `/networkuser` |
| HsmAllgroups | `hsm:allgroups` | `/hsm:allgroups` |
| HsmEntrustnshieldgroup | `hsm:entrustnshieldgroup` | `/hsm:entrustnshieldgroup` |
| HsmThaleslunagroup | `hsm:thaleslunagroup` | `/hsm:thaleslunagroup` |

## Deeply Nested / dict Fields

Several resources contain complex nested structures modelled as `dict[str, Any] | None`:

- `Admingroup`: `admin_set_commands`, `admin_show_commands`, `admin_toplevel_commands`,
  `cloud_set_commands`, `cloud_show_commands`, `database_set_commands`, `database_show_commands`,
  `dhcp_set_commands`, `dhcp_show_commands`, `dns_set_commands`, `dns_show_commands`,
  `dns_toplevel_commands`, `docker_set_commands`, `docker_show_commands`, `grid_set_commands`,
  `grid_show_commands`, `inactivity_lockout_setting`, `licensing_set_commands`,
  `licensing_show_commands`, `lockout_setting`, `machine_control_toplevel_commands`,
  `networking_set_commands`, `networking_show_commands`, `password_setting`, `saml_setting`,
  `security_set_commands`, `security_show_commands`, `trouble_shooting_toplevel_commands`,
  `user_access` (all complex nested schema types)
- `Adminuser`: `ssh_keys` (array of nested SSH key objects)
- `CertificateAuthservice`: `ca_certificates`, `ocsp_responders`, `test_ocsp_responder_settings`
- `RadiusAuthservice`: `check_radius_server_settings`, `servers`
- `TacacsplusAuthservice`: `check_tacacsplus_server_settings`, `servers`
- `LdapAuthService`: `check_ldap_server_settings`, `ea_mapping`, `servers`
- `SamlAuthservice`: `idp`
- `AdAuthService`: `domain_controllers`
- `HsmEntrustnshieldgroup`: `entrustnshield_hsm`, `refresh_hsm`, `test_hsm_status`
- `HsmThaleslunagroup`: `thalesluna`, `refresh_hsm`, `test_hsm_status`

## Singleton / Read-only Observations

- `Authpolicy`: singleton-style - only one record per WAPI. Standard CRUD methods exist
  but `create` and `delete` will fail at the WAPI level.
- `HsmAllgroups`: aggregate read-only view. Only field is `groups` (list of group refs).
  `create` and `delete` will fail at WAPI level.
- `Cacertificate`: entirely read-only (all fields are readOnly). No writable fields.
- `LocaluserAuthservice`: all non-_ref fields are readOnly (singleton for the built-in local
  user auth service). Read and update via PUT may be the only viable operations.

## Ftpuser: `username` not `name`

The swagger schema uses `username` (not `name`) as the primary identifier for `Ftpuser`.
Default return fields are `["username", "comment"]` - note discrepancy from plan's `["name", "comment"]`.

## Networkuser: `user_status` is readOnly

The plan specified `["user_status", "address"]` as extra default_return_fields for Networkuser,
but `user_status` is readOnly. It is included in default_return_fields (readable on GET) but
stripped on PUT/POST.

## Python Keyword Collision

- No `type` field collisions found in the security domain schemas.
