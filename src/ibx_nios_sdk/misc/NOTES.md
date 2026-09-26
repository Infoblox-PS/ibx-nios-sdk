# Misc Domain Notes

## Objects

### Standard CRUD
- `allendpoints` - read-only aggregate, no POST/PUT/DELETE
- `bfdtemplate` - full CRUD; `uuid` is read-only
- `capacityreport` - read-only
- `csvimporttask` - GET + PUT only (no POST/DELETE); `stop` function via `/csvimporttask/{ref}/stop`
- `datacollectioncluster` - full CRUD; `name` and `uuid` are read-only
- `db_objects` - read-only
- `dbsnapshot` - GET + PUT only; `rollback_db_snapshot` and `save_db_snapshot` functions
- `deleted_objects` - read-only
- `dxl:endpoint` - full CRUD; `uuid` and certificate-validity fields are read-only
- `kerberoskey` - GET + DELETE only (no POST/PUT)
- `outbound:cloudclient` - GET + PUT only; `uuid` is read-only
- `pxgrid:endpoint` - full CRUD; `uuid` and certificate-validity fields are read-only
- `ruleset` - full CRUD; `uuid` is read-only
- `scavengingtask` - read-only
- `scheduledtask` - GET + PUT + DELETE; many read-only fields
- `syslog:endpoint` - full CRUD; `uuid` is read-only
- `taxii` - GET + PUT only; `uuid`, `ipv4addr`, `ipv6addr`, `name` are read-only
- `tftpfiledir` - full CRUD; `is_synced_to_gm` and `last_modify` are read-only

### Deeply nested (typed as `dict[str, Any] | None`)
- `DxlEndpoint.template_instance`, `DxlEndpoint.clear_outbound_worker_log`, `DxlEndpoint.test_broker_connectivity`
- `Dbsnapshot.rollback_db_snapshot`, `Dbsnapshot.save_db_snapshot`
- `PxgridEndpoint.publish_settings`, `PxgridEndpoint.subscribe_settings`, `PxgridEndpoint.template_instance`, `PxgridEndpoint.test_connection`
- `SyslogEndpoint.template_instance`, `SyslogEndpoint.test_syslog_connection`

### Function-only (plain classes - NOT WapiResource subclasses)
- `Fileop` - all access via `POST /fileop?_function=<name>` (many typed methods)
- `Search` - global search via `GET /search` (query parameters)

## Fileop typed methods
- `upload_init()` → `uploadinit`
- `upload_certificate()` → `uploadcertificate`
- `csv_import()` → `csv_import`
- `csv_export()` → `csv_export`
- `csv_snapshot_file()` → `csv_snapshot_file`
- `download_complete()` → `downloadcomplete`
- `downloadcertificate()` → `downloadcertificate`
- `call(function, **kwargs)` - generic dispatch
