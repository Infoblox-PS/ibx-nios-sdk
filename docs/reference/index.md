# API Reference

Auto-generated reference for every public class, method, and model in the
SDK. Pages are organized by domain - pick the one you need on the left, or
use search.

The reference content is extracted directly from the source code on every
docs build, so it always matches the installed SDK.

## Client

::: ibx_nios_sdk.client.NiosClient

## Core Building Blocks

### HTTP Client

The low-level transport. You normally won't touch this directly - it's
created by `NiosClient` and shared across services.

::: ibx_nios_sdk._http.HttpClient

### Resource Base Class

Every resource on every domain inherits from `WapiResource`. The standard
`list`, `list_page`, `get`, `create`, `update`, `delete`, and
`call_function` methods are all defined here.

::: ibx_nios_sdk._resource.WapiResource

### Query Builder & Pagination

::: ibx_nios_sdk._query
    options:
      show_root_heading: false
      show_root_toc_entry: false

::: ibx_nios_sdk._paging
    options:
      show_root_heading: false
      show_root_toc_entry: false

### Object-Type Restrictions

The generated table of operations each WAPI object type refuses, consulted by
`WapiResource` before every read, create, update, and delete. Regenerate it with
`tools/refresh_object_restrictions.py` after refreshing the schema snapshot.

::: ibx_nios_sdk._restrictions
    options:
      show_root_heading: false
      show_root_toc_entry: false

### Exceptions

::: ibx_nios_sdk._exceptions
    options:
      show_root_heading: false
      show_root_toc_entry: false
