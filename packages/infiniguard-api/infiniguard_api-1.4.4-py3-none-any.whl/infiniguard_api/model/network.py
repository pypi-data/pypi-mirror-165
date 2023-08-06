from marshmallow import Schema, ValidationError, post_load, pre_dump, validate, validates_schema
from marshmallow.fields import Boolean, Int, List, Nested, String

from infiniguard_api.controller.network import host, interfaces
from infiniguard_api.model import custom_fields, validators
from infiniguard_api.model.base_schema import MessageSchema, PaginatedResponseSchema, NonPaginatedResponseSchema
from infiniguard_api.model.validators import MIN_VLAN, MAX_VLAN, MIN_MTU, MAX_MTU

MTU_DEFAULT = 1500


class HostSchema(Schema):
    hostname = String(description='DDE Host Name', example='host0')
    search_domain = List(String(required=True),
                         attribute='dns_search_path',
                         description='List of search domains',
                         example=['localhost', 'blah.net'])
    dns_servers = List(custom_fields.IpAddress(required=True),
                       description='List of DNS servers',
                       example=['8.8.8.8', '8.8.8.4'])
    # read only field, set it to interface gateway when ext_host_ip is set to YES
    # we do not handle error besides anything syscli returns
    default_gateway = custom_fields.IpAddress(attribute='default_gateway',
                                              description='Default gateway IP',
                                              example='10.10.10.1')


class HostCreateUpdateSchema(HostSchema):
    @post_load
    def convert_from_request(self, in_data, **kwargs):
        host.convert_from_request(in_data)
        if in_data.get('default_gateway', None) and in_data['default_gateway'] is not None:
            raise ValidationError(
                'Default Gateway is automatically set from an interface gateway with ext_host_ip as YES')
        return in_data

    @pre_dump
    def convert_to_response(self, out_data, **kwargs):
        return host.convert_to_response(out_data)


class HostResponseSchema(Schema):
    hostname = String(description='DDE Host Name', example='host0')
    search_domain = List(String(),
                         attribute='dns_search_path',
                         description='List of search domains',
                         example=['localhost', 'blah.net'])
    dns_servers = List(String(),
                       description='List of DNS servers',
                       example=['8.8.8.8', '8.8.8.4'])
    # read only field, set it to interface gateway when ext_host_ip is set to YES
    # we do not handle error besides anything syscli returns
    default_gateway = String(attribute='default_gateway',
                             description='Default gateway IP',
                             example='10.10.10.1')


class HostResponse(MessageSchema):
    result = Nested(HostResponseSchema)

    @pre_dump
    def convert_to_response(self, out_data, **kwargs):
        result = host.convert_to_response(out_data.get('result', {}))
        out_data['result'] = result
        return out_data


class HostCreateUpdate(MessageSchema):
    result = Nested(HostCreateUpdateSchema)


class StaticRouteSchema(Schema):
    network = custom_fields.IpAddress(required=True,
                                      description='Destination network',
                                      example='10.10.10.0')
    mask = custom_fields.Netmask(attribute='netmask',
                                 required=True,
                                 description='Destination netmask',
                                 example='255.255.255.0')
    gateway = custom_fields.IpAddress(
        required=True, description='Gateway IP address', example='10.10.10.1')
    devname = String(description='Device Name', example='dev0')


class StaticRouteResponse(MessageSchema):
    result = Nested(StaticRouteSchema)


class StaticRoutesResponse(PaginatedResponseSchema):
    result = List(Nested(StaticRouteSchema),
                  example=[
                      {
                          "gateway": "10.10.10.1",
                          "mask": "255.255.255.0",
                          "network": "10.10.10.0"
                      }
                  ])


class DeviceSchema(Schema):
    devname = String(attribute='Name', required=True,
                     description='Device Name', example='dev0')
    max_speed = String(attribute='MaxSpeed', required=True,
                       description='Maximum Speed', example='10GbE')
    intf_names = List(String(), dump_only=True,
                      description='List of interface names',
                      example=['dev0', 'dev1'],
                      allow_none=True)


class DeviceResponse(MessageSchema):
    result = Nested(DeviceSchema, only=['devname', 'max_speed'])


class DevicesResponse(PaginatedResponseSchema):
    result = List(Nested(DeviceSchema, only=['devname', 'max_speed']),
                  example=[
                      {
                          "devname": "p4p1",
                          "max_speed": "10GbE"
                      }
                  ])


class BaseInterfaceSchema(Schema):
    ip_address = custom_fields.IpAddress(description='IP Address', example='10.10.10.10')
    netmask = custom_fields.Netmask(
        description='Netmask', example='255.255.255.0')
    gateway = custom_fields.IpAddress(
        description='Gateway', example='10.10.10.1')
    segments = List(String(description='Only allow the specified traffic types on this interface',
                           example='data, replication'), validate=validators.validate_traffic_type,
                    data_key='traffic_type')
    mtu = Int(validate=validate.Range(min=MIN_MTU, max=MAX_MTU), missing=MTU_DEFAULT,
              description='MTU for the interface', example=1500)
    ext_host_ip = Boolean(data_key='ext_dde_ip',
                          description='Whether or not this is the default DDE interface', example=True)
    nat = custom_fields.IpAddress(description='NAT IP address')

    type = String(validate=validate.OneOf(
        ['bond', 'port', 'Bond', 'Port']), required=True, example='bond', data_key='interface_type')

    # Only for bond type
    mode = String(validate=validate.OneOf(
        ['rr', 'ab', 'lacp', 'RR', 'AB', 'LACP']),
        description='Bond mode', example='lacp')  # Default is RR, only when selecting interface_type='bond'
    slaves = List(String,
                  data_key='members',
                  description='List of bond members',
                  example=['p4p1', 'p4p2'])

    @post_load
    def convert_from_request(self, data, **kwargs):
        return interfaces.convert_from_request(data)


class CreateInterfaceSchema(BaseInterfaceSchema):
    devname = String(description='Device Name', example='em3', required=True)

    vlan = Int(validate=validate.Range(min=MIN_VLAN, max=MAX_VLAN),
               description="Virtual LAN ID for the interface", example=2)

    @validates_schema
    def _validates_schema(self, data, **kwargs):
        validators.validate_intfname(data['devname'], interface_type=data['type'])

        if not all(k in data for k in ("ip_address", "netmask", "gateway")):
            raise ValidationError(
                '{ip_address, netmask, gateway} fields must all be provided')

        if '.' in data['devname'] and data.get('vlan', None):
            raise ValidationError("VLAN ID can not be present in both devname and vlan parameters.", 'vlan')

        if data['type'].lower() == 'bond':
            if not data.get('slaves'):
                raise ValidationError("Missing data for required field.", 'members')

            if not len(data['slaves']) >= 2:
                raise ValidationError("Should include at least two ports", 'members')
            for member in data['slaves']:
                if not validators.is_valid_port(member):
                    raise ValidationError("All members must have the pattern: 'p4p1'", 'members')
        else:
            if data.get('mode') or data.get('slaves'):
                raise ValidationError("'mode' and 'members' fields are not applicable when creating an "
                                      "interface of type 'port'")


class QueryInterfaceSchema(BaseInterfaceSchema):
    devname = String(description='Device name', example='p7p1')
    intfname = String(description='Interface name', example='p7p1.5:1')
    operstate = String(description='Interface operational state')
    carrier = String(description='Interface link status')
    configured = Boolean(description='Has the interface been configured')
    routes = List(Nested(StaticRouteSchema),
                  description='Routes for the interface', example=0)


class InterfaceResponse(NonPaginatedResponseSchema):
    result = Nested(QueryInterfaceSchema)


class InterfacesResponse(PaginatedResponseSchema):
    result = List(Nested(QueryInterfaceSchema),
                  example=[
                      {
                          "carrier": "up",
                          "configured": True,
                          "default_gateway": "NO",
                          "devname": "p4p4",
                          "ext_host_ip": "YES",
                          "gateway": "172.20.63.254",
                          "intfname": "p4p4:1",
                          "ip_address": "172.20.45.226",
                          "mtu": 1500,
                          "netmask": "255.255.224.0",
                          "operstate": "up",
                          "segments": [
                              "ALL"
                          ],
                          "type": "Port"
                      }])


schema_classes = [
    HostSchema,
    HostResponse,
    HostCreateUpdate,
    StaticRouteSchema,
    StaticRouteResponse,
    StaticRoutesResponse,
    DeviceSchema,
    DeviceResponse,
    DevicesResponse,
    BaseInterfaceSchema,
    InterfaceResponse,
    InterfacesResponse,
]
