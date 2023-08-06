# Scapy
from scapy.packet import Packet
# Internal
from bof.layers.raw_scapy import chicken as scapy_chicken
from bof.packet import BOFPacket
from bof.base import BOFProgrammingError, to_property

class ChickenPacket(BOFPacket):

    #-------------------------------------------------------------------------#
    # Public                                                                  #
    #-------------------------------------------------------------------------#

    def __init__(self, _pkt:bytes=None, **kwargs) -> None:
        self._scapy_pkt = scapy_chicken.Chicken(_pkt=_pkt)
        self._set_fields(**kwargs)
