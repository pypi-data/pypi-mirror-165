import re

from marshmallow import ValidationError


MIN_VLAN = 2
MAX_VLAN = 4094
MIN_MTU = 576
MAX_MTU = 9000
MIN_INTF = 1
MAX_INTF = 10


def is_valid_port(devname):
    return bool(re.match(r'^p\dp\d$', devname))


def is_valid_bond(devname):
    return bool(re.match(r'^bond\d+$', devname))


def validate_devname(devname, interface_type=None):
    if interface_type:
        if interface_type.lower() == 'port' and not is_valid_port(devname):
            raise ValidationError("Must have the pattern: 'p4p1'", 'devname')
        elif interface_type.lower() == 'bond' and not is_valid_bond(devname):
            raise ValidationError("Must have the pattern: 'bond1'", 'devname')
    else:
        if not (is_valid_bond(devname) or is_valid_port(devname)):
            raise ValidationError("Must have the pattern of 'p4p1' or 'bond0", 'devname')


def validate_traffic_type(traffic_type):
    if not set(traffic_type) <= {'any', 'replication', 'data'}:
        raise ValidationError("Must be a combination of {replication, data, any}", 'traffic_type')


def validate_intfname(intfname, only_intf=False, interface_type=None):
    """Function to validate a device name.

    :param intfname: Device name. The general format is <label>[.<vlanid>]:<vifno> where
        label:  alphanumeric string
        vlanid: VLAN ID is an optional field and can range from 2 to 4094.
        vifno:  virtual interface number, which is used to distinguish each set of
            network layer (L3) values, i.e. IP address and netmask values.
            It can range from 1 to possibly 99, depending on actual systems.
    :param interface_type: 'port' or 'bond'. If None, allows devname to be of either form (bond0 or p4p1).
    :raise ValidationError: if the input is not a valid device name
    """
    if not intfname:
        raise ValidationError('No interface name or device name specified')

    if intfname.count(':') > 1:
        raise ValidationError("Only one interface number can appear in devname", 'devname')
    if intfname.count('.') > 1:
        raise ValidationError("Only one VLAN ID can appear in devname", 'devname')

    parts = intfname.split(':')
    devname_vlanid = parts[0]
    numparts = len(parts)
    if only_intf and numparts != 2:
        raise ValidationError("full interface name is required <devname>[.<vlandid>]:<intf_num>")

    intfnum = parts[1] if numparts == 2 else None
    if intfnum and not MIN_INTF <= int(intfnum) <= MAX_INTF:
        raise ValidationError(f"Interface number must be between {MIN_INTF} and {MAX_INTF} (inclusive), "
                              f"if provided in devname", 'devname')

    parts = devname_vlanid.split('.')
    devname = parts[0]
    validate_devname(devname, interface_type)

    vlanid = parts[1] if len(parts) == 2 else None
    if vlanid and not MIN_VLAN <= int(vlanid) <= MAX_VLAN:
        raise ValidationError(f"VLAN ID must be between {MIN_VLAN} and {MAX_VLAN} (inclusive), if provided in devname",
                              'devname')

    return intfname

