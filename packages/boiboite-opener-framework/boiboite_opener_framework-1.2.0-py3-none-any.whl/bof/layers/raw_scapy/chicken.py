from scapy.fields import ByteField, StrField, IntEnumField
from scapy.packet import Packet

class Chicken(Packet):
    name = "Chicken"
    fields_desc = [
        ByteField("length", None),
        IntEnumField("type", 1,
                     {1: "Bresse", 2: "Berry", 3: "Bastard"}),
        StrField("sound", "")
    ]
    def post_build(self, p, pay):
        p = (len(p)).to_bytes(1, byteorder='big') + p[1:]
        return p + pay
