from scapy.all import *


# IEC104 asdu
class asdu_head(Packet):
    name = "asdu_head"
    fields_desc = [XByteField("TypeID", 0x0d),
                   XByteField("SQ", 0x81),
                   XByteField("Cause", 0x05),
                   XByteField("OA", 0x00),
                   LEShortField("Addr", 0x0001)]


class CP56Time(Packet):
    name = "CP56Time"
    # 1991-02-19_10:30:1.237
    fields_desc = [
        XShortField("Ms", 0xd504),
        XByteField("Min", 0x1e),
        XByteField("Hour", 0xa),
        XByteField("Day", 0x13),
        XByteField("Month", 0x02),
        XByteField("Year", 0x5b),
    ]


class asdu_infobj_13(Packet):
    name = "M_ME_NC_1"
    fields_desc = [
        X3BytesField("IOA", 0x01),
        XIntField("Value", 0x00000000),
        XByteField("QDS", 0xf1)]


class asdu_infobj_45(Packet):
    name = "C_SC_NA_1"
    fields_desc = [
        X3BytesField("IOA", 0x23),
        XByteField("SCO", 0x80)]


class asdu_infobj_46(Packet):
    name = "C_DC_NA_1"
    fields_desc = [
        X3BytesField("IOA", 0x23),
        XByteField("DCO", 0x80)]


class asdu_infobj_47(Packet):
    name = "C_RC_NA_1"
    fields_desc = [
        X3BytesField("IOA", 0x23),
        XByteField("RCO", 0x80)]


class asdu_infobj_48(Packet):
    name = "C_SE_NA_1"
    fields_desc = [
        X3BytesField("IOA", 0x23),
        StrField("Value", '', fmt="H", remain=0),
        XByteField("QOS", 0x80)]


class asdu_infobj_49(Packet):
    name = "C_SE_NB_1"
    fields_desc = [
        X3BytesField("IOA", 0x23),
        StrField("Value", '', fmt="H", remain=0),
        XByteField("QOS", 0x80)]


class asdu_infobj_50(Packet):
    name = "C_SE_NC_1"
    fields_desc = [
        X3BytesField("IOA", 0x23),
        StrField("Value", '', fmt="f", remain=0),
        XByteField("QOS", 0x80)]


class asdu_infobj_51(Packet):
    name = "C_BO_NA_1"
    fields_desc = [
        X3BytesField("IOA", 0x23),
        StrField("Value", '', fmt="I", remain=0)]


class asdu_infobj_58(Packet):
    name = "C_SC_TA_1"
    fields_desc = [
        X3BytesField("IOA", 0x23),
        XByteField("SCO", 0x80),
        PacketField("CP56Time", CP56Time, Packet)]


class asdu_infobj_59(Packet):
    name = "C_DC_TA_1"
    fields_desc = [
        X3BytesField("IOA", 0x23),
        XByteField("DCO", 0x80),
        PacketField("CP56Time", CP56Time, Packet)]


class asdu_infobj_60(Packet):
    name = "C_RC_TA_1"
    fields_desc = [
        X3BytesField("IOA", 0x23),
        XByteField("RCO", 0x80),
        PacketField("CP56Time", CP56Time, Packet)]


class asdu_infobj_61(Packet):
    name = "C_SE_TA_1"
    fields_desc = [
        X3BytesField("IOA", 0x23),
        StrField("Value", '', fmt="H", remain=0),
        XByteField("QOS", 0x80),
        PacketField("CP56Time", CP56Time, Packet)]


class asdu_infobj_62(Packet):
    name = "C_SE_TB_1"
    fields_desc = [
        X3BytesField("IOA", 0x23),
        StrField("Value", '', fmt="H", remain=0),
        XByteField("QOS", 0x80),
        PacketField("CP56Time", CP56Time, Packet)]


class asdu_infobj_63(Packet):
    name = "C_SE_TC_1"
    fields_desc = [
        X3BytesField("IOA", 0x23),
        StrField("Value", '', fmt="f", remain=0),
        XByteField("QOS", 0x80),
        PacketField("CP56Time", CP56Time, Packet)]


class asdu_infobj_64(Packet):
    name = "C_BO_TA_1"
    fields_desc = [
        X3BytesField("IOA", 0x23),
        StrField("Value", '', fmt="I", remain=0),
        PacketField("CP56Time", CP56Time, Packet)]


class asdu_infobj_100(Packet):
    name = "C_IC_NA_1"
    fields_desc = [
        X3BytesField("IOA", 0x00),
        XByteField("Operation", 0x14)]


class asdu_infobj_101(Packet):
    name = "C_CI_NA_1"
    fields_desc = [
        X3BytesField("IOA", 0x00),
        XByteField("Operation", 0x05)]


class asdu_infobj_103(Packet):
    name = "C_CS_NA_1"
    fields_desc = [
        X3BytesField("IOA", 0x00),
        PacketField("CP56Time", CP56Time, Packet)]


# IEC104 apci
class i_frame(Packet):
    name = "i_frame"
    fields_desc = [XByteField("START", 0x68),
                   XByteField("ApduLen", None),
                   LEShortField("Type", 0x00),
                   LEShortField("Tx", 0x0000),
                   LEShortField("Rx", 0x0000),
                   ]

    def post_build(self, p, pay):
        if self.ApduLen is None:
            l = len(pay) + 4
            p = p[:1] + struct.pack("!B", l) + p[2:]
        return p + pay


class s_frame(Packet):
    name = "s_frame"
    fields_desc = [XByteField("START", 0x68),
                   XByteField("ApduLen", 0x04),
                   LEShortField("Type", 0x01),
                   LEShortField("Rx", 0x0000)]


class u_frame(Packet):
    name = "u_frame"
    fields_desc = [XByteField("START", 0x68),
                   XByteField("ApduLen", 0x04),
                   LEShortField("Type", 0x03),
                   LEShortField("UType", 0x0000)]


# help Scapy to build links between layers

def iec_bind_layers(asdu_id):
    if asdu_id == 13:
        bind_layers(i_frame, asdu_infobj_13)
        bind_layers(asdu_infobj_13, Padding)
    elif asdu_id == 45:
        bind_layers(i_frame, asdu_infobj_45)
        bind_layers(asdu_infobj_45, Padding)
    elif asdu_id == 46:
        bind_layers(i_frame, asdu_infobj_46)
        bind_layers(asdu_infobj_46, Padding)
    elif asdu_id == 47:
        bind_layers(i_frame, asdu_infobj_47)
        bind_layers(asdu_infobj_47, Padding)
    elif asdu_id == 48:
        bind_layers(i_frame, asdu_infobj_48)
        bind_layers(asdu_infobj_48, Padding)
    elif asdu_id == 49:
        bind_layers(i_frame, asdu_infobj_49)
        bind_layers(asdu_infobj_49, Padding)
    elif asdu_id == 50:
        bind_layers(i_frame, asdu_infobj_50)
        bind_layers(asdu_infobj_50, Padding)
    elif asdu_id == 51:
        bind_layers(i_frame, asdu_infobj_51)
        bind_layers(asdu_infobj_51, Padding)
    elif asdu_id == 58:
        bind_layers(i_frame, asdu_infobj_58)
        bind_layers(asdu_infobj_58, Padding)
    elif asdu_id == 59:
        bind_layers(i_frame, asdu_infobj_59)
        bind_layers(asdu_infobj_59, Padding)
    elif asdu_id == 60:
        bind_layers(i_frame, asdu_infobj_60)
        bind_layers(asdu_infobj_60, Padding)
    elif asdu_id == 61:
        bind_layers(i_frame, asdu_infobj_61)
        bind_layers(asdu_infobj_61, Padding)
    elif asdu_id == 62:
        bind_layers(i_frame, asdu_infobj_62)
        bind_layers(asdu_infobj_62, Padding)
    elif asdu_id == 63:
        bind_layers(i_frame, asdu_infobj_63)
        bind_layers(asdu_infobj_63, Padding)
    elif asdu_id == 64:
        bind_layers(i_frame, asdu_infobj_64)
        bind_layers(asdu_infobj_64, Padding)
    elif asdu_id == 100:
        bind_layers(i_frame, asdu_infobj_100)
        bind_layers(asdu_infobj_100, Padding)
    elif asdu_id == 101:
        bind_layers(i_frame, asdu_infobj_101)
        bind_layers(asdu_infobj_101, Padding)
    elif asdu_id == 103:
        bind_layers(i_frame, asdu_infobj_103)
        bind_layers(asdu_infobj_103, Padding)

    else:
        print('ASDU_TypeID is not supported')


