# CLI Utilities

The `ibx-nios-sdk` ships 10 command-line utilities for common NIOS Grid operations.
Install them via:

```bash
pip install 'ibx-nios-sdk[cli]'
```

All commands support `--help` (or `-h`) and accept the same core connection options:
Grid Manager URL, admin username, and WAPI version.  Passwords are read from the
`NIOS_PASSWORD` environment variable or prompted securely at runtime.

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `NIOS_GRID_URL` | Grid Manager URL (e.g. `https://grid.example.com`) | - |
| `NIOS_USERNAME` | Admin username | `admin` |
| `NIOS_PASSWORD` | Admin password (falls back to `getpass` prompt) | - |
| `NIOS_WAPI_VERSION` | WAPI API version string | `2.14` |

---

## Commands

### `nios-csvexport`

Export any NIOS WAPI object type to a local CSV file using the `fileop csv_export` endpoint.

```text
Usage: nios-csvexport [OPTIONS]

Options:
  Required Parameters:
    -g, --grid-mgr TEXT  Infoblox Grid Manager hostname or URL  [required]
    -f, --filename TEXT  Output CSV file path to write  [required]
  Optional Parameters:
    -u, --username TEXT  Infoblox admin username  [default: admin]
    -w, --wapi-ver TEXT  Infoblox WAPI version  [default: 2.14]
    -o, --obj TEXT       WAPI object type to export (e.g. network, record:a)
                         [default: network]
  Logging Parameters:
    --debug              Enable verbose debug logging
  -h, --help             Show this message and exit.
```

**Example:**

```bash
nios-csvexport -g 192.168.1.2 -f networks.csv -o network
nios-csvexport -g 192.168.1.2 -f a_records.csv -o record:a --debug
```

---

### `nios-csvimport`

Import a local CSV file into NIOS via the `fileop uploadinit` / `csv_import` flow.
The import task ID is printed so progress can be tracked via the `csvimporttask` WAPI object.

```text
Usage: nios-csvimport [OPTIONS]

Options:
  Required Parameters:
    -g, --grid-mgr TEXT           Infoblox Grid Manager hostname or URL  [required]
    -f, --filename TEXT           Local CSV file path to upload  [required]
    -o, --operation [insert|override|merge|delete|custom]
                                  Import operation mode  [required]
  Optional Parameters:
    -u, --username TEXT           Infoblox admin username  [default: admin]
    -w, --wapi-ver TEXT           Infoblox WAPI version  [default: 2.14]
  Logging Parameters:
    --debug                       Enable verbose debug logging
  -h, --help                      Show this message and exit.
```

**Example:**

```bash
nios-csvimport -g 192.168.1.2 -f networks.csv -o MERGE
nios-csvimport -g 192.168.1.2 -f new_hosts.csv -o INSERT --debug
```

---

### `nios-get-file`

Download a Grid member configuration file (DNS config, DHCP config, traffic capture, etc.)
via the `fileop getfile` endpoint.

```text
Usage: nios-get-file [OPTIONS]

Options:
  Required Parameters:
    -g, --grid-mgr TEXT  Infoblox Grid Manager hostname or URL  [required]
    -m, --member TEXT    Grid member hostname to retrieve file from  [required]
    -f, --filename TEXT  Output file path to write the downloaded file  [required]
  Optional Parameters:
    -u, --username TEXT  Infoblox admin username  [default: admin]
    -t, --cfg-type [dns_cache|dns_cfg|dhcp_cfg|dhcpv6_cfg|traffic_capture_file|dns_stats|dns_recursing_cache]
                         Configuration type  [default: DNS_CFG]
    -w, --wapi-ver TEXT  Infoblox WAPI version  [default: 2.14]
  Logging Parameters:
    --debug              Enable verbose debug logging
  -h, --help             Show this message and exit.
```

**Example:**

```bash
nios-get-file -g 192.168.1.2 -m ns1.example.com -f dns_cfg.txt
nios-get-file -g 192.168.1.2 -m ns1.example.com -t DHCP_CFG -f dhcp_cfg.txt
```

---

### `nios-get-log`

Download a Grid member log file (syslog, audit log, etc.) via the `fileop get_log_files`
endpoint.

```text
Usage: nios-get-log [OPTIONS]

Options:
  Required Parameters:
    -g, --grid-mgr TEXT  Infoblox Grid Manager hostname or URL  [required]
    -m, --member TEXT    Grid member hostname to retrieve log from  [required]
    -f, --filename TEXT  Output file path to write the downloaded log  [required]
  Optional Parameters:
    -u, --username TEXT  Infoblox admin username  [default: admin]
    -l, --log-type LOG_TYPE
                         Log type: SYSLOG | AUDITLOG | MSMGMTLOG | DELTALOG |
                         OUTBOUND | PTOPLOG | DISCOVERY_CSV_ERRLOG  [default: SYSLOG]
    -n, --node-type [active|backup]
                         HA node to retrieve the log from  [default: ACTIVE]
    -r, --rotated-logs   Include rotated log files (SYSLOG only)
    -w, --wapi-ver TEXT  Infoblox WAPI version  [default: 2.14]
  Logging Parameters:
    --debug              Enable verbose debug logging
  -h, --help             Show this message and exit.
```

**Example:**

```bash
nios-get-log -g 192.168.1.2 -m ns1.example.com -f syslog.txt
nios-get-log -g 192.168.1.2 -m ns1.example.com -l AUDITLOG -f audit.txt
```

---

### `nios-get-supportbundle`

Download a full diagnostic support bundle from a Grid member via the
`fileop get_support_bundle` endpoint.

```text
Usage: nios-get-supportbundle [OPTIONS]

Options:
  Required Parameters:
    -g, --grid-mgr TEXT  Infoblox Grid Manager hostname or URL  [required]
    -m, --member TEXT    Grid member hostname to retrieve bundle from  [required]
    -f, --filename TEXT  Output file path to write the support bundle  [required]
  Optional Parameters:
    -u, --username TEXT  Infoblox admin username  [default: admin]
    -r, --rotated-logs   Include rotated log files in the bundle
    -l, --log-files      Include log files in the bundle
    -w, --wapi-ver TEXT  Infoblox WAPI version  [default: 2.14]
  Logging Parameters:
    --debug              Enable verbose debug logging
  -h, --help             Show this message and exit.
```

**Example:**

```bash
nios-get-supportbundle -g 192.168.1.2 -m ns1.example.com -f bundle.tar.gz
nios-get-supportbundle -g 192.168.1.2 -m ns1.example.com -f bundle.tar.gz -l -r
```

---

### `nios-grid-backup`

Download a full Grid database backup to a local file via the `fileop getgriddata` endpoint.

```text
Usage: nios-grid-backup [OPTIONS]

Options:
  Required Parameters:
    -g, --grid-mgr TEXT  Infoblox Grid Manager hostname or URL  [required]
  Optional Parameters:
    -u, --username TEXT  Infoblox admin username  [default: admin]
    -f, --filename TEXT  Output file path for the backup  [default: database.bak]
    -w, --wapi-ver TEXT  Infoblox WAPI version  [default: 2.14]
  Logging Parameters:
    --debug              Enable verbose debug logging
  -h, --help             Show this message and exit.
```

**Example:**

```bash
nios-grid-backup -g 192.168.1.2 -f grid_$(date +%Y%m%d).bak
nios-grid-backup -g 192.168.1.2  # writes to database.bak
```

---

### `nios-grid-restore`

Upload a local backup file and restore the NIOS Grid via the `fileop restoredatabase`
endpoint.

!!! warning "Destructive operation"
    Grid restore replaces the running database. Ensure you have a valid backup before
    proceeding.

```text
Usage: nios-grid-restore [OPTIONS]

Options:
  Required Parameters:
    -g, --grid-mgr TEXT           Infoblox Grid Manager hostname or URL  [required]
    -f, --filename TEXT           Local backup file path to upload  [required]
  Optional Parameters:
    -u, --username TEXT           Infoblox admin username  [default: admin]
    -r, --restore-mode [NORMAL|FORCED|CLONE]
                                  Grid restore mode  [default: NORMAL]
    -k, --keep                    Keep existing Grid IP (not from backup)
    -w, --wapi-ver TEXT           Infoblox WAPI version  [default: 2.14]
  Logging Parameters:
    --debug                       Enable verbose debug logging
  -h, --help                      Show this message and exit.
```

**Example:**

```bash
nios-grid-restore -g 192.168.1.2 -f grid_20240101.bak
nios-grid-restore -g 192.168.1.2 -f grid_20240101.bak -r FORCED --keep
```

---

### `nios-certificate`

Upload or download SSL certificates for NIOS Grid members via the `fileop` endpoint.
This is a multi-command tool with `upload` and `download` subcommands.

```text
Usage: nios-certificate [OPTIONS] COMMAND [ARGS]...

Commands:
  upload    Upload a certificate file to an Infoblox Grid member.
  download  Download a certificate from an Infoblox Grid member.
```

**Upload subcommand options:** `-g/--grid-mgr`, `-m/--member`, `-f/--filename`
(required); `-t/--cert-type` (ADMIN, CAPTIVE_PORTAL, SFNT_CLIENT_CERT, IFMAP_DHCP,
EAP_CA, TAE_CA; default: ADMIN); `-u/--username`, `-w/--wapi-ver`, `--debug`.

**Example:**

```bash
nios-certificate upload -g 192.168.1.2 -m gm.example.com -f server.pem
nios-certificate download -g 192.168.1.2 -m gm.example.com -f cert_out.pem
nios-certificate upload -g 192.168.1.2 -m gm.example.com -f ca.pem -t EAP_CA
```

---

### `nios-restart-service`

Restart NIOS protocol services grid-wide or on a specific member.
Omit `--member` for a grid-wide restart.

```text
Usage: nios-restart-service [OPTIONS]

Options:
  Required Parameters:
    -g, --grid-mgr TEXT  Infoblox Grid Manager hostname or URL  [required]
  Optional Parameters:
    -u, --username TEXT  Infoblox admin username  [default: admin]
    -m, --member TEXT    Specific Grid member hostname (omit for grid-wide)
    -s, --services TEXT  Service(s) to restart - may be repeated  [default: DNS, DHCP]
    -r, --restart-option [RESTART_IF_NEEDED|FORCE_RESTART|RELOAD_ALL|RESTART_ALL]
                         Restart trigger policy  [default: RESTART_IF_NEEDED]
    -w, --wapi-ver TEXT  Infoblox WAPI version  [default: 2.14]
  Logging Parameters:
    --debug              Enable verbose debug logging
  -h, --help             Show this message and exit.
```

**Example:**

```bash
nios-restart-service -g 192.168.1.2                         # grid-wide DNS+DHCP
nios-restart-service -g 192.168.1.2 -m ns1.example.com -s DNS
nios-restart-service -g 192.168.1.2 -s DNS -s DHCP -r FORCE_RESTART
```

---

### `nios-restart-status`

Display the current service restart status for all Grid members in a tabular format.

```text
Usage: nios-restart-status [OPTIONS]

Options:
  Required Parameters:
    -g, --grid-mgr TEXT  Infoblox Grid Manager hostname or URL  [required]
  Optional Parameters:
    -u, --username TEXT  Infoblox admin username  [default: admin]
    -w, --wapi-ver TEXT  Infoblox WAPI version  [default: 2.14]
  Logging Parameters:
    --debug              Enable verbose debug logging
  -h, --help             Show this message and exit.
```

**Example:**

```bash
nios-restart-status -g 192.168.1.2
nios-restart-status -g 192.168.1.2 -u readonly_admin
```
