# Grid Domain Notes

## WAPI Type Discrepancies

- All 44 WAPI types match the swagger paths verbatim.
- `grid:member:cloudapi` is the WAPI type for `GridMemberCloudapi` (path `/grid:member:cloudapi`).
- `membercloudsync` and `memberdfp` use no colon (flat name).

## Python Keyword Collisions

- `Extensibleattributedef.type_` aliases to WAPI `"type"` field.
- `LicenseGridwide.type_` aliases to WAPI `"type"` field.

## Restartservicestatus - field names

The `Restartservicestatus` model exposes `dhcp_status`, `dns_status`, `member`,
and `reporting_status`. There is **no** `restart_status` field in the WAPI
schema. Scripts that display restart status should use `dhcp_status` and/or
`dns_status`. The `manage_members.py list-restart-status` command was found to
access `s.restart_status` - that is a script bug; the model is correct.

## Deeply Nested Fields

Several objects have nested sub-objects that are typed as `dict[str, Any]` for simplicity:
- `Grid`: `automated_traffic_capture_setting`, `consent_banner_setting`, `csp_api_config`, etc.
- `Member`: `additional_ip_list`, `bgp_as`, `capture_traffic_control`, `node_info`, etc.
- `GridDns`: `allow_query`, `allow_transfer`, `attack_mitigation`, etc.
- `GridDhcpproperties`: `options`, `logic_filter_rules`, etc.
