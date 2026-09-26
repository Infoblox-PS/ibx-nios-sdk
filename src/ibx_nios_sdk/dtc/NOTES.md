# DTC Domain - Implementation Notes

## WAPI type mapping

| SDK class | WAPI type |
|-----------|-----------|
| `Dtc` | `dtc` (get+put only, no POST/DELETE; has function sub-paths) |
| `DtcServer` | `dtc:server` |
| `DtcPool` | `dtc:pool` |
| `DtcLbdn` | `dtc:lbdn` |
| `DtcTopology` | `dtc:topology` |
| `DtcTopologyRule` | `dtc:topology:rule` (get+put, no POST/DELETE) |
| `DtcTopologyLabel` | `dtc:topology:label` (get only) |
| `DtcCertificate` | `dtc:certificate` (get only) |
| `DtcObject` | `dtc:object` (get+put, no POST/DELETE) |
| `DtcAllrecords` | `dtc:allrecords` (get+put, read-only aggregate) |
| `DtcMonitor` | `dtc:monitor` (get+put, no POST/DELETE) |
| `DtcMonitorHttp` | `dtc:monitor:http` |
| `DtcMonitorIcmp` | `dtc:monitor:icmp` |
| `DtcMonitorPdp` | `dtc:monitor:pdp` |
| `DtcMonitorSip` | `dtc:monitor:sip` |
| `DtcMonitorSnmp` | `dtc:monitor:snmp` |
| `DtcMonitorTcp` | `dtc:monitor:tcp` |
| `DtcRecordA` | `dtc:record:a` |
| `DtcRecordAaaa` | `dtc:record:aaaa` |
| `DtcRecordCname` | `dtc:record:cname` |
| `DtcRecordNaptr` | `dtc:record:naptr` |
| `DtcRecordSrv` | `dtc:record:srv` |

## `Dtc` - global config object

`/dtc` only has GET (list) and `/dtc/{reference}` has GET+PUT. No POST or DELETE.
The `Dtc` schema properties are all function-schema refs (not plain fields):
`add_certificate`, `dtc_get_object_grid_state`, `dtc_object_disable`,
`dtc_object_enable`, `generate_ea_topology_db`, `import_maxminddb`, `query`.
These are modelled as `dict[str, Any] | None` - they represent function call
schemas that are invoked via POST to sub-paths like `/dtc/add_certificate`.

## `DtcMonitor` - base monitor type

`/dtc:monitor` is get+put only (no POST/DELETE). It has a `type` field (Python
keyword collision → `type_`).

## `DtcTopologyLabel` - fully read-only

All non-`_ref` fields are readOnly. GET only.

## `DtcCertificate` - fully read-only

All non-`_ref` fields are readOnly. GET only - certificates are managed via
the `Dtc.add_certificate` function path.

## `DtcObject` - mostly read-only aggregate

All non-`_ref` and non-`extattrs` fields are readOnly. GET+PUT.

## `DtcPool` nested fields

`lb_dynamic_ratio_alternate` and `lb_dynamic_ratio_preferred` reference
complex schemas (`DtcPoolLbDynamicRatioAlternate`, etc.) - modelled as
`dict[str, Any] | None`.

`consolidated_monitors`, `monitors`, `servers` are arrays of complex nested
objects - modelled as `list[dict[str, Any]] | None`.

## `DtcLbdn` nested fields

`auth_zones`, `patterns`, `pools`, `types` are arrays - modelled as
`list[str] | None` (for auth_zones/patterns/types) or
`list[dict[str, Any]] | None` (for pools - they include priority/ratio).

## `DtcServer.monitors` and `DtcPool.monitors`

Arrays of monitor references with associated health info - modelled as
`list[dict[str, Any]] | None`.

## `DtcMonitorSnmp.oids`

Array of SNMP OID structs - modelled as `list[dict[str, Any]] | None`.

## `DtcTopologyRule.destination` and `.sources`

Arrays of destination/source structs - modelled as `list[dict[str, Any]] | None`.

## `DtcMonitor.type` and `DtcAllrecords.type`

Python keyword collision: `type` → `type_` with `Field(alias="type")`.
