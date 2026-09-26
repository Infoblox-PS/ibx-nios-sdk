# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Grid - NIOS Grid object.

All properties from ``components.schemas.Grid`` in the v2.14 grid swagger.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "restart_status",
        "service_status",
        "uuid",
    }
)


class Grid(BaseModel):
    """NIOS Grid object."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    allow_recursive_deletion: Literal["NOBODY", "ALL", "SUPERUSERS"] | str | None = Field(
        default=None,
        description="The property to allow recursive deletion. Determines the users who can choose to perform recursive deletion on networks or zones from the GUI only.",
    )
    audit_log_format: Literal["DETAILED", "BRIEF", "WAPI_DETAILED"] | str | None = Field(
        default=None, description="Determines the audit log format."
    )
    audit_to_syslog_enable: bool | None = Field(
        default=None,
        description="If set to True, audit log messages are also copied to the syslog.",
    )
    automated_traffic_capture_setting: dict[str, Any] | None = Field(
        default=None, description="Settings controlling automated DNS traffic capture."
    )
    consent_banner_setting: dict[str, Any] | None = Field(default=None)
    csp_api_config: dict[str, Any] | None = Field(default=None)
    csp_grid_setting: dict[str, Any] | None = Field(default=None)
    deny_mgm_snapshots: bool | None = Field(
        default=None,
        description="If set to True, the managed Grid will not send snapshots to the Multi-Grid Master.",
    )
    descendants_action: dict[str, Any] | None = Field(
        default=None, description="Action to apply to descendant objects when this object changes."
    )
    dns_resolver_setting: dict[str, Any] | None = Field(
        default=None, description="DNS resolver settings used by the member."
    )
    dscp: int | None = Field(
        default=None,
        description="The DSCP value. Valid values are integers between 0 and 63 inclusive.",
    )
    email_setting: dict[str, Any] | None = Field(
        default=None, description="SMTP / email notification settings."
    )
    enable_federation: bool | None = Field(
        default=None,
        description="Determines if the Cloud Grid Management feature is enabled or not. Test Setting will be performed for any change in enable_federation.",
    )
    enable_force_sync_join_token_to_gmc: bool | None = Field(
        default=None,
        description="Determines if the force sync join token from GM to GMC is enabled or not.",
    )
    enable_gui_api_for_lan_vip: bool | None = Field(
        default=None,
        description="If set to True, GUI and API access are enabled on the LAN/VIP port and MGMT port (if configured).",
    )
    enable_lom: bool | None = Field(
        default=None, description="Determines if the LOM functionality is enabled or not."
    )
    enable_member_redirect: bool | None = Field(
        default=None, description="Determines redirections is enabled or not for members."
    )
    enable_recycle_bin: bool | None = Field(
        default=None, description="Determines if the Recycle Bin is enabled or not."
    )
    enable_rir_swip: bool | None = Field(
        default=None, description="Determines if the RIR/SWIP support is enabled or not."
    )
    external_syslog_backup_servers: list[dict[str, Any]] | None = Field(
        default=None, description="The list of external backup syslog servers."
    )
    external_syslog_server_enable: bool | None = Field(
        default=None, description="If set to True, external syslog servers are enabled."
    )
    http_proxy_server_setting: dict[str, Any] | None = Field(default=None)
    informational_banner_setting: dict[str, Any] | None = Field(default=None)
    is_grid_visualization_visible: bool | None = Field(
        default=None, description="If set to True, graphical visualization of the Grid is enabled."
    )
    lockout_setting: dict[str, Any] | None = Field(
        default=None, description="Account lockout settings (failed-login limits, lockout window)."
    )
    lom_users: list[dict[str, Any]] | None = Field(
        default=None, description="The list of LOM users."
    )
    mgm_strict_delegate_mode: bool | None = Field(
        default=None,
        description="Determines if strict delegate mode for the Grid managed by the Master Grid is enabled or not.",
    )
    ms_setting: dict[str, Any] | None = Field(default=None)
    name: str | None = Field(default=None, description="The grid name.")
    nat_groups: list[str] | None = Field(
        default=None,
        description="The list of all Network Address Translation (NAT) groups configured on the Grid.",
    )
    ntp_setting: dict[str, Any] | None = Field(
        default=None, description="NTP client/server settings."
    )
    objects_changes_tracking_setting: dict[str, Any] | None = Field(default=None)
    password_setting: dict[str, Any] | None = Field(
        default=None, description="Password policy settings (length, history, complexity)."
    )
    restart_banner_setting: dict[str, Any] | None = Field(default=None)  # read-only
    restart_status: dict[str, Any] | str | None = Field(
        default=None, description="The restart status for the Grid."
    )
    rpz_hit_rate_interval: int | None = Field(
        default=None,
        description="The time interval (in seconds) that determines how often the appliance calculates the RPZ hit rate.",
    )
    rpz_hit_rate_max_query: int | None = Field(
        default=None,
        description="The maximum number of incoming queries between the RPZ hit rate checks.",
    )
    rpz_hit_rate_min_query: int | None = Field(
        default=None,
        description="The minimum number of incoming queries between the RPZ hit rate checks.",
    )
    scheduled_backup: dict[str, Any] | None = Field(default=None)
    secret: str | None = Field(
        default=None, description="The shared secret of the Grid. This is a write-only attribute."
    )
    security_banner_setting: dict[str, Any] | None = Field(default=None)
    security_setting: dict[str, Any] | None = Field(default=None)  # read-only
    service_status: (
        Literal["FAILED", "UNKNOWN", "OFFLINE", "INACTIVE", "WARNING", "WORKING"] | str | None
    ) = Field(default=None, description="Determines overall service status of the Grid.")
    snmp_setting: dict[str, Any] | None = Field(default=None, description="SNMP agent settings.")
    support_bundle_download_timeout: int | None = Field(
        default=None, description="Support bundle download timeout in seconds."
    )
    syslog_facility: (
        Literal[
            "DAEMON",
            "LOCAL0",
            "LOCAL1",
            "LOCAL2",
            "LOCAL3",
            "LOCAL4",
            "LOCAL5",
            "LOCAL6",
            "LOCAL7",
        ]
        | str
        | None
    ) = Field(
        default=None,
        description="If 'audit_to_syslog_enable' is set to True, the facility that determines the processes and daemons from which the log messages are generated.",
    )
    syslog_servers: list[dict[str, Any]] | None = Field(
        default=None, description="The list of external syslog servers."
    )
    syslog_size: int | None = Field(
        default=None, description="The maximum size for the syslog file expressed in megabytes."
    )
    threshold_traps: list[dict[str, Any]] | None = Field(
        default=None,
        description="Determines the list of threshold traps. The user can only change the values for each trap or remove traps.",
    )
    time_zone: str | None = Field(
        default=None,
        description='The time zone of the Grid. The UTC string that represents the time zone, such as "US/Eastern".',
    )
    token_usage_delay: int | None = Field(
        default=None, description="The delayed usage (in minutes) of a permission token."
    )
    traffic_capture_auth_dns_setting: dict[str, Any] | None = Field(
        default=None, description="Authoritative-DNS criteria for automated traffic capture."
    )
    traffic_capture_chr_setting: dict[str, Any] | None = Field(
        default=None, description="Cache-hit-ratio criteria for automated traffic capture."
    )
    traffic_capture_qps_setting: dict[str, Any] | None = Field(
        default=None, description="Queries-per-second criteria for automated traffic capture."
    )
    traffic_capture_rec_dns_setting: dict[str, Any] | None = Field(
        default=None, description="Recursive-DNS criteria for automated traffic capture."
    )
    traffic_capture_rec_queries_setting: dict[str, Any] | None = Field(
        default=None, description="Recursive-queries criteria for automated traffic capture."
    )
    trap_notifications: list[dict[str, Any]] | None = Field(
        default=None, description="Determines configuration of the trap notifications."
    )
    updates_download_member_config: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of member configuration structures, which provides information and settings for configuring the member that is responsible for downloading updates.",
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    vpn_port: int | None = Field(default=None, description="The VPN port.")
    control_ip_address: object | None = Field(
        default=None, description="Use this function to control selected IP addresses."
    )
    download_join_file: object | None = Field(
        default=None,
        description="This function retrieves join file for the grid. See the file downloading sample code in the manual {samplecode:download} and the fileop object for more information.",
    )
    empty_recycle_bin: object | None = Field(default=None, description="Empty the recycle bin.")
    generate_join_info: object | None = Field(
        default=None, description="This function retrieves join information for the grid."
    )
    generate_tsig_key: object | None = Field(
        default=None, description="This function is used to generate TSIG key."
    )
    get_all_template_vendor_id: object | None = Field(
        default=None,
        description="Use this function to get all unique vendor identifiers for the outbound templates.",
    )
    get_grid_revert_status: object | None = Field(
        default=None,
        description="This function is used to retrieve the revert status of the Infoblox Grid.",
    )
    get_rpz_threat_details: object | None = Field(
        default=None, description="Requests RPZ threat details through the ThreatStop RESTful API."
    )
    get_template_schema_versions: object | None = Field(
        default=None, description="Get all schema versions for the RESTful API templates."
    )
    join: object | None = Field(
        default=None, description="Join an Infoblox appliance to an existing grid."
    )
    join_mgm: object | None = Field(
        default=None, description="This function allows a Grid to join the Multi-Grid Master."
    )
    join_mgm_mod2: object | None = Field(
        default=None, description="This function allows a Grid to join the Sub-Grid."
    )
    leave_mgm: object | None = Field(
        default=None, description="This function allows a Grid to leave the Multi-Grid Master."
    )
    member_upgrade: object | None = Field(
        default=None,
        description="Use this function to upgrade a single member that was reverted during the staged upgrade process or to revert a single member if it does not behave properly after an upgrade.",
    )
    publish_changes: object | None = Field(
        default=None,
        description="Publish configuration changes to all Grid members or to a particular one.",
    )
    query_fqdn_on_member: object | None = Field(
        default=None, description="Invokes dig command on a member for a specific FQDN."
    )
    requestrestartservicestatus: object | None = Field(
        default=None,
        description="Use this function to request the Grid service status. This function will refresh the restartservicestatus object.",
    )
    restartservices: object | None = Field(
        default=None,
        description="This function controls the Grid services. Please note that fields 'member_order', 'service_option' and 'sequential_delay' are deprecated from NIOS-9.0.7 version onwards. Instead, use 'mode', 'services' and 'restart_setting' of the grid:dns or grid:dhcpproperties.",
    )
    skip_member_upgrade: object | None = Field(
        default=None,
        description="This function allows the specified member to skip the upgrade process.",
    )
    start_discovery: object | None = Field(
        default=None, description="Use this function to start the discovery on selected objects."
    )
    test_syslog_backup_server_connection: object | None = Field(
        default=None,
        description="This function can be used to test the connection to the external backup syslog server.",
    )
    test_syslog_connection: object | None = Field(
        default=None, description="Use this function to test a connection to the syslog server."
    )
    upgrade: object | None = Field(
        default=None,
        description="This function provides control over the Grid upgrade. The upgrade process normally is as follows: 1) Upload the upgrade file using the set_upgrade_file function call in object fileop 2) call this function with 'action' set to 'UPLOAD', this will prepare the uploaded file for deployment 3) call this function with 'action' set to 'DISTRIBUTION_START' which will start the Grid distribution process. 4) call this function with 'action' set to 'UPGRADE_TEST_START' to run the test upgrade (mandatory...",
    )
    upgrade_group_now: object | None = Field(
        default=None,
        description="This function is used to run the immediate upgrade of the specified group.",
    )
    upload_keytab: object | None = Field(
        default=None,
        description="This function is used to upload the keytab file to the server that is not assigning the keys.",
    )
    validatecertificates: object | None = Field(
        default=None,
        description="Validates idns certificates and all certificates from /infoblox/security/certs with openssl",
    )
