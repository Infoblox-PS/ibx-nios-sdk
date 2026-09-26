# Threatinsight Domain - Implementation Notes

## WAPI Type Discrepancies (swagger ground truth)

The implementation plan listed several default_return_fields that do not exist in the
v2.14 swagger. Actual swagger-verified fields are used instead:

| Class | Plan default_return_fields | Swagger-verified fields used |
|---|---|---|
| ThreatinsightAllowlist | `["name", "fqdn", "type", "comment"]` | `["fqdn", "type", "comment"]` - no `name` field in swagger |
| ThreatinsightCloudclient | `["enable", "host", "last_synced"]` | `["enable"]` - no `host` or `last_synced` in swagger |
| ThreatinsightInsightAllowlist | `["name", "fqdn", "type", "comment"]` | `["version"]` - only `uuid` (readOnly) + `version` (readOnly) exist |
| ThreatinsightModuleset | `["version", "last_updated"]` | `["version"]` - no `last_updated` in swagger |

## WAPI Type: insight_allowlist

The plan tentatively listed `threatinsight:insightallowlist` but swagger dictates
`threatinsight:insight_allowlist` (with underscore). The implementation uses the
swagger path `/threatinsight:insight_allowlist`.

## Operation Availability

| Resource | GET list | POST | GET ref | PUT | DELETE |
|---|---|---|---|---|---|
| ThreatinsightAllowlist | yes | yes | yes | yes | yes |
| ThreatinsightCloudclient | yes | - | yes | yes | - |
| ThreatinsightInsightAllowlist | yes | - | yes | - | - |
| ThreatinsightModuleset | yes | - | yes | - | - |

`ThreatinsightCloudclient`, `ThreatinsightInsightAllowlist`, and `ThreatinsightModuleset`
are essentially read-only (no create/delete). `ThreatinsightCloudclient` supports PUT to
toggle settings. The `WapiResource` base class provides all methods; the swagger operations
above reflect what NIOS actually accepts.

## ThreatinsightAllowlist.type_

The `type` field (SYSTEM|CUSTOM enum) shadows the Python builtin `type`.
It is modelled as `type_` with `Field(alias="type")` and is in `READONLY_FIELDS`.

## ThreatinsightCloudclient.force_refresh

`force_refresh` is marked `writeOnly: true` in swagger - included in the model as a
writable bool but will not appear in GET responses.

## ThreatinsightInsightAllowlist

Despite the plan's description mentioning `name`, `fqdn`, `type`, `comment`, the actual
swagger schema for `threatinsight:insight_allowlist` contains only `_ref`, `uuid`
(readOnly), and `version` (readOnly). This object appears to be a read-only aggregate.
