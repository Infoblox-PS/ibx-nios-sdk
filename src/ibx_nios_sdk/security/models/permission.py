# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Permission - NIOS permission.

All 7 properties from ``components.schemas.Permission`` in the v2.14 security
swagger are represented here.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Permission(BaseModel):
    """NIOS permission.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    group: str | None = Field(
        default=None, description="The name of the admin group this permission applies to."
    )
    object: str | None = Field(
        default=None,
        description="A reference to a WAPI object, which will be the object this permission applies to.",
    )
    permission: Literal["DENY", "READ", "WRITE"] | str | None = Field(
        default=None, description="The type of permission."
    )
    resource_type: (
        Literal[
            "CLUSTER",
            "MEMBER",
            "MEMBER_CLOUD",
            "SUB_GRID",
            "SUB_GRID_NETWORK_VIEW_PARENT",
            "SG_NETWORK_VIEW",
            "SG_IPV4_NETWORK",
            "SG_IPV6_NETWORK",
            "MSSERVER",
            "VIEW",
            "ZONE",
            "A",
            "AAAA",
            "ALIAS",
            "CNAME",
            "DNAME",
            "MX",
            "PTR",
            "SRV",
            "TXT",
            "HOST",
            "BULKHOST",
            "NAPTR",
            "TLSA",
            "CAA",
            "SVCB",
            "HTTPS",
            "Unknown",
            "SHARED_RECORD_GROUP",
            "SHARED_A",
            "SHARED_AAAA",
            "SHARED_MX",
            "SHARED_SRV",
            "SHARED_TXT",
            "SHARED_CNAME",
            "NETWORK_VIEW",
            "NETWORK",
            "IPV6_NETWORK",
            "NETWORK_CONTAINER",
            "IPV6_NETWORK_CONTAINER",
            "RANGE",
            "IPV6_RANGE",
            "FIXED_ADDRESS",
            "IPV6_FIXED_ADDRESS",
            "ROAMING_HOST",
            "DHCP_MAC_FILTER",
            "SHARED_NETWORK",
            "IPV6_SHARED_NETWORK",
            "TEMPLATE",
            "IPV6_TEMPLATE",
            "NETWORK_TEMPLATE",
            "IPV6_NETWORK_TEMPLATE",
            "RANGE_TEMPLATE",
            "IPV6_RANGE_TEMPLATE",
            "FIXED_ADDRESS_TEMPLATE",
            "IPV6_FIXED_ADDRESS_TEMPLATE",
            "OPTION_SPACE",
            "RESTORABLE_OPERATION",
            "CSV_IMPORT_TASK",
            "DHCP_LEASE_HISTORY",
            "IPV6_DHCP_LEASE_HISTORY",
            "GRID_FILE_DIST_PROPERTIES",
            "MEMBER_FILE_DIST_PROPERTIES",
            "FILE_DIST_DIRECTORY",
            "HSM_GROUP",
            "GRID_AAA_PROPERTIES",
            "AAA_EXTERNAL_SERVICE",
            "NETWORK_DISCOVERY",
            "SCHEDULE_TASK",
            "MS_SUPERSCOPE",
            "MEMBER_DNS_PROPERTIES",
            "MEMBER_DHCP_PROPERTIES",
            "MEMBER_SECURITY_PROPERTIES",
            "MEMBER_ANALYTICS_PROPERTIES",
            "RESTART_SERVICE",
            "GRID_DNS_PROPERTIES",
            "GRID_DHCP_PROPERTIES",
            "GRID_REPORTING_PROPERTIES",
            "GRID_SECURITY_PROPERTIES",
            "IMC_PROPERTIES",
            "IMC_SITE",
            "IMC_AVP",
            "GRID_ANALYTICS_PROPERTIES",
            "RULESET",
            "DNS64_SYNTHESIS_GROUP",
            "DASHBOARD_TASK",
            "REPORTING_DASHBOARD",
            "REPORTING_SEARCH",
            "OCSP_SERVICE",
            "CA_CERTIFICATE",
            "RESPONSE_POLICY_ZONE",
            "RESPONSE_POLICY_RULE",
            "DHCP_FINGERPRINT",
            "DEFINED_ACL",
            "FIREEYE_PUBLISH_ALERT",
            "HOST_ADDRESS",
            "IPV6_HOST_ADDRESS",
            "PORT_CONTROL",
            "DEVICE",
            "KERBEROS_KEY",
            "BFD_TEMPLATE",
            "MS_ADSITES_DOMAIN",
            "IDNS_LBDN",
            "IDNS_LBDN_RECORD",
            "IDNS_POOL",
            "IDNS_SERVER",
            "IDNS_TOPOLOGY",
            "IDNS_MONITOR",
            "IDNS_CERTIFICATE",
            "IDNS_GEO_IP",
            "TENANT",
            "RECLAMATION",
            "SUPER_HOST",
            "ADD_A_RR_WITH_EMPTY_HOSTNAME",
            "DATACOLLECTOR_CLUSTER",
            "DELETED_OBJS_INFO_TRACKING",
            "SAML_AUTH_SERVICE",
            "VLAN_VIEW",
            "VLAN_RANGE",
            "VLAN_OBJECTS",
        ]
        | str
        | None
    ) = Field(
        default=None,
        description="The type of resource this permission applies to. If 'object' is set, the permission is going to apply to child objects of the specified type, for example if 'object' was set to an authoritative zone reference and 'resource_type' was set to 'A', the permission would apply to A Resource Records within the specified zone.",
    )
    role: str | None = Field(
        default=None, description="The name of the role this permission applies to."
    )
