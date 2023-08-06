from collections import OrderedDict

from infiniguard_api.model import validators, custom_fields
from infiniguard_api.model.base_schema import PaginationSchema, ErrorSchema, PaginatedResponseSchema
from marshmallow import Schema, validate, validates_schema, pre_dump, pre_load, ValidationError
from marshmallow.fields import String, Boolean, Int, Nested, List, Dict


class ManyOrOneSchema(Schema):
    @pre_dump
    def wrap_indata(self, indata):
        if type(indata) is not OrderedDict:
            return indata
        key = self.__class__.__name__.replace('Schema', '')
        val = indata.get(key, None)
        if val and type(val) is OrderedDict:
            indata[key] = [val]
        return indata


class L3InterfaceSchema(Schema):
    Name = String()
    IP = String()
    Mask = String()
    DEFGW = String()
    Routes = String()
    Segments = String()
    hostIp = String()


class SlaveSchema(Schema):
    Name = String()
    Speed = String()


class InterfaceSchema(Schema):
    Name = String()
    BootProtocol = String()
    MTU = Int()
    Speed = String()
    Type = String()
    Options = String()
    Slaves = List(Nested(SlaveSchema))
    L3Interfaces = List(Nested(L3InterfaceSchema))
    Operstate = String()
    Carrier = String()


class StaticRouteSchema(Schema):
    IP = String()
    Mask = String()
    Gateway = String()


class CustomerInterfaceSchema(Schema):
    Name = String()
    MaxSpeed = String()


class DNS_ServerSchema(Schema):
    DNS_Server = String()


class HostSchema(Schema):
    Name = String()
    Domain = String()
    DefaultGateway = String()
    DNS_Servers = List(Nested(DNS_ServerSchema))
    DNS_Cache = String()


class NetworkCfgSchema(Schema):
    Host = Nested(HostSchema)
    CustomerInterfaces = List(Nested(CustomerInterfaceSchema))
    StaticRoutes = List(Nested(StaticRouteSchema))
    ConfiguredInterfaces = List(Nested(InterfaceSchema))
    RuntimeInterfaces = List(Nested(InterfaceSchema))
    NetworkCfg = Nested('self', ref='NetworkCfgSchema')


class NetcfgPaginatedSchema(PaginatedResponseSchema):
    result = Nested(NetworkCfgSchema)
    message = String()
