"""NFStream plugin: end a TCP flow as soon as the conversation is over, instead of waiting 5 s idle.
Used in BOTH training (.pcap) and live detection, so flows are cut the same way."""
from nfstream import NFPlugin


class EndOnRstFin(NFPlugin):
    """RST seen -> flow ends now (scan probes: SYN -> RST).
    FIN seen from both sides -> flow ends on the next packet (the last ACK)."""

    def on_init(self, packet, flow):
        flow.udps.fin_src = int(packet.fin and packet.direction == 0)
        flow.udps.fin_dst = int(packet.fin and packet.direction == 1)
        if packet.rst:
            flow.expiration_id = -1          # -1 = custom expiration (NFStream docs)

    def on_update(self, packet, flow):
        if packet.rst:
            flow.expiration_id = -1
            return
        if flow.udps.fin_src and flow.udps.fin_dst:   # both FINs already seen: this is the last ACK
            flow.expiration_id = -1
            return
        if packet.fin:
            if packet.direction == 0:
                flow.udps.fin_src = 1
            else:
                flow.udps.fin_dst = 1
