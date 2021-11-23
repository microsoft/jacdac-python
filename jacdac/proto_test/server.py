from jacdac.pack import jdpack
from ..bus import Bus, Server
from ..packet import JDPacket
from .constants import *


class ProtoTestServer(Server):
    def __init__(self, bus: Bus) -> None:
        super().__init__(bus, JD_SERVICE_CLASS_PROTO_TEST)
        self.rw_bool = 0
        self.rw_i32 = 0
        self.rw_u32 = 0
        self.rw_str = ""
        self.rw_bytes = bytearray(0)
        self.rw_u8_string = [0, ""]

    def handle_packet(self, pkt: JDPacket):
        cmd = pkt.service_command
        rw_bool = self.handle_reg(pkt, JD_PROTO_TEST_REG_RW_BOOL,
                                  JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RW_BOOL], self.rw_bool)
        if rw_bool != self.rw_bool:
            self.rw_bool = rw_bool
            self.send_event(JD_PROTO_TEST_EV_E_BOOL, jdpack(
                JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RW_BOOL], self.rw_bool))
        self.handle_reg(pkt, JD_PROTO_TEST_REG_RO_BOOL,
                        JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RO_BOOL], self.rw_bool)
        if cmd == JD_PROTO_TEST_CMD_C_BOOL:
            [self.rw_bool] = pkt.unpack(JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_CMD_C_BOOL])

        rw_i32 = self.handle_reg(
            pkt, JD_PROTO_TEST_REG_RW_I32, JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RW_I32], self.rw_i32)
        if rw_i32 != self.rw_i32:
            self.rw_i32 = rw_i32
            self.send_event(JD_PROTO_TEST_EV_E_I32, jdpack(
                JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RW_I32], self.rw_i32))
        self.handle_reg(pkt, JD_PROTO_TEST_REG_RO_I32,
                        JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RO_I32], self.rw_i32)
        if cmd == JD_PROTO_TEST_CMD_C_I32:
            [self.rw_i32] = pkt.unpack(JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_CMD_C_I32])

        rw_u32 = self.handle_reg(
            pkt, JD_PROTO_TEST_REG_RW_U32, JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RW_U32], self.rw_u32)
        if rw_u32 != self.rw_u32:
            self.rw_u32 = rw_u32
            self.send_event(JD_PROTO_TEST_EV_E_U32, jdpack(
                JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RW_U32], self.rw_u32))
        self.handle_reg(pkt, JD_PROTO_TEST_REG_RO_U32,
                        JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RO_U32], self.rw_u32)
        if cmd == JD_PROTO_TEST_CMD_C_U32:
            [self.rw_u32] = pkt.unpack(JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_CMD_C_U32])

        rw_str = self.handle_reg(pkt, JD_PROTO_TEST_REG_RW_STRING,
                                 JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RW_STRING], self.rw_str)
        if rw_str != self.rw_str:
            self.rw_str = rw_str
            self.send_event(JD_PROTO_TEST_EV_E_STRING, jdpack(
                JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RW_STRING], self.rw_str))
        self.handle_reg(pkt, JD_PROTO_TEST_REG_RO_STRING,
                        JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RO_STRING], self.rw_str)
        if cmd == JD_PROTO_TEST_CMD_C_STRING:
            [self.rw_str] = pkt.unpack(JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_CMD_C_STRING])

        rw_bytes = self.handle_reg(pkt, JD_PROTO_TEST_REG_RW_BYTES,
                                 JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RW_BYTES], self.rw_bytes)
        if rw_bytes != self.rw_bytes:
            self.rw_bytes = rw_bytes
            self.send_event(JD_PROTO_TEST_EV_E_BYTES, jdpack(
                JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RW_BYTES], self.rw_bytes))
        self.handle_reg(pkt, JD_PROTO_TEST_REG_RO_BYTES,
                        JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_REG_RO_BYTES], self.rw_bytes)
        if cmd == JD_PROTO_TEST_CMD_C_BYTES:
            [self.rw_bytes] = pkt.unpack(JD_PROTO_TEST_PACK_FORMATS[JD_PROTO_TEST_CMD_C_BYTES])

        return super().handle_packet(pkt)


"""    
    export class ProtocolTestServer extends JDServiceServer {
    private rwBytes: JDRegisterServer<[Uint8Array]>

    constructor() {
        super(SRV_PROTO_TEST)

        this.init<[boolean]>(
            ProtoTestReg.RwBool,
            ProtoTestReg.RoBool,
            ProtoTestCmd.CBool,
            ProtoTestEvent.EBool,
            false
        )
        this.init<[number]>(
            ProtoTestReg.RwI32,
            ProtoTestReg.RoI32,
            ProtoTestCmd.CI32,
            ProtoTestEvent.EI32,
            0
        )
        this.init<[number]>(
            ProtoTestReg.RwU32,
            ProtoTestReg.RoU32,
            ProtoTestCmd.CU32,
            ProtoTestEvent.EU32,
            0
        )
        this.init<[string]>(
            ProtoTestReg.RwString,
            ProtoTestReg.RoString,
            ProtoTestCmd.CString,
            ProtoTestEvent.EString,
            ""
        )
        this.rwBytes = this.init<[Uint8Array]>(
            ProtoTestReg.RwBytes,
            ProtoTestReg.RoBytes,
            ProtoTestCmd.CBytes,
            ProtoTestEvent.EBytes,
            new Uint8Array(0)
        )
        this.init<[number, number, number, number]>(
            ProtoTestReg.RwI8U8U16I32,
            ProtoTestReg.RoI8U8U16I32,
            ProtoTestCmd.CI8U8U16I32,
            ProtoTestEvent.EI8U8U16I32,
            0,
            0,
            0,
            0
        )
        this.init<[number, string]>(
            ProtoTestReg.RwU8String,
            ProtoTestReg.RoU8String,
            ProtoTestCmd.CU8String,
            ProtoTestEvent.EU8String,
            0,
            ""
        )

        this.addCommand(
            ProtoTestCmd.CReportPipe,
            this.handleReportPipe.bind(this)
        )
    }

    private init<TValues extends any[]>(
        rwi: number,
        roi: number,
        ci: number,
        ei: number,
        ...values: TValues
    ) {
        const rw = this.addRegister(rwi, values)
        const ro = this.addRegister(roi, rw.values())
        rw.on(CHANGE, () => {
            ro.setValues(rw.values())
            this.sendEvent(ei, rw.data)
        })
        this.addCommand(ci, pkt =>
            rw.setValues(jdunpack(pkt.data, rw.specification.packFormat))
        )
        return rw
    }

    private async handleReportPipe(pkt: Packet) {
        const pipe = OutPipe.from(this.device.bus, pkt, true)
        await pipe.respondForEach(this.rwBytes.data, (b: number) => {
            const buf = new Uint8Array(1)
            buf[0] = b
            return jdpack<[Uint8Array]>("b", [buf])
        })
    }
}
"""
