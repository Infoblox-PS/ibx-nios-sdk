# Threatprotection domain - swagger-vs-reality notes + resource pattern

## Per-object file layout

For each new WAPI object type `<wapi:type>`:

1. **Model** → `src/ibx_nios_sdk/threatprotection/models/<snake_case>.py` containing:
   - A `READONLY_FIELDS: frozenset[str]` of field names the swagger marks
     `readOnly: true`. These are stripped on PUT.
   - The main BaseModel class with `ConfigDict(populate_by_name=True, extra="allow")`.
   - `ref: str | None = Field(default=None, alias="_ref")`.
   - Every field from the swagger, typed as `<type> | None = None`.

2. **Resource** → `src/ibx_nios_sdk/threatprotection/_<snake_case>.py`:
   - Subclass `WapiResource[<Model>]`.
   - `_wapi_type` = exact WAPI type string.
   - `_model` = the pydantic class.
   - `_default_return_fields` = identity/human-readable fields.
   - `_readonly_fields` = `set(<ModelModule>.READONLY_FIELDS)`.

3. **Service wiring** → add `@cached_property` in `threatprotection/_service.py`.

4. **Tests** → `tests/threatprotection/test_<snake_case>.py`.

## WAPI type note

The swagger path uses `threatprotection:grid:rule` (not `grid:threatprotection:rule`
as listed in some documentation). The swagger path is authoritative.

## Approximated / complex fields

| Resource | Field | Swagger type | Reason approximated |
|---|---|---|---|
| ThreatprotectionGridRule | `config` | `ThreatprotectionGridRuleConfig` object | Nested config with params array of complex objects; typed as `dict[str, Any] \| None`. |
| ThreatprotectionProfileRule | `config` | `ThreatprotectionProfileRuleConfig` object | Same pattern; typed as `dict[str, Any] \| None`. |
| ThreatprotectionRule | `config` | `ThreatprotectionRuleConfig` object | Same pattern; typed as `dict[str, Any] \| None`. |
| ThreatprotectionRuletemplate | `default_config` | `ThreatprotectionRuletemplateDefaultConfig` object | Same pattern; typed as `dict[str, Any] \| None`. |
| ThreatprotectionStatistics | `stat_infos` | array of `ThreatprotectionStatisticsStatInfos` | Complex nested stat objects; typed as `list[dict[str, Any]] \| None`. |
| ThreatprotectionGridRule | `allowed_actions` | array of strings | Typed as `list[str] \| None`. |
| ThreatprotectionRuleset | `used_by` | array | Typed as `list[str] \| None`. |
| ThreatprotectionRuletemplate | `allowed_actions` | array of strings | Typed as `list[str] \| None`. |

## Read-only resources (list/get only, no write operations)

- `ThreatprotectionRulecategory` - GET collection and GET by ref only (no PUT/DELETE).
- `ThreatprotectionRuletemplate` - GET collection and GET by ref only.
- `ThreatprotectionStatistics` - GET collection and GET by ref only.

## Partially read-only resources (no POST/DELETE)

- `ThreatprotectionProfileRule` - GET + PUT only, no POST/DELETE.
- `ThreatprotectionRule` - GET + PUT only, no POST/DELETE.
