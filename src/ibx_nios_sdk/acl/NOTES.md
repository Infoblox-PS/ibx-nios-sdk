# ACL Domain Notes

## Namedacl

### validate_acl_items

The swagger schema `NamedaclValidateAclItems` has no defined properties
(`"type": "object", "properties": {}`). It is modelled as
`dict[str, Any] | None` to preserve round-trip fidelity until the schema
is clarified.

### access_list / exploded_access_list

Both fields reference `NamedaclAccessList` which is a concrete schema with
6 defined properties. It is modelled as `NamedaclAccessList` in
`models/namedacl.py`. Note that `exploded_access_list` is read-only
(readOnly: true).
