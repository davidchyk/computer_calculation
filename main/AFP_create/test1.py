# afp_builder.py
import struct, zlib, time, pathlib

HDR_LEN   = 0x50         # 80 байт
DEV_SIZE  = 32
WIRE_SIZE = 16

def _timestamp64():
    """мікросекунди з 1970-01-01 → 8-байтний little-endian"""
    return int(time.time()*1_000_000).to_bytes(8, 'little')

def build_afp(devices, wires, grid_step=1):
    """devices:  [{'lib':0x0DBB,'x':0.0,'y':0.0,'rot':1.0,'flags':1,'pins':2}, …]
       wires:    [{'src':(0,2),'dst':(0,1),'bend':(0.5,0.0)}, …]"""

    # ── 1. Порожній 80-байтний заголовок ───────────────────────────
    hdr = bytearray(HDR_LEN)
    hdr[0x00:0x08] = _timestamp64()
    hdr[0x08:0x0C] = b'\x40\x00\x04\x00'           # постійна сигнатура
    hdr[0x42:0x44] = struct.pack('<H', grid_step)  # GridStep
    hdr[0x46:0x48] = struct.pack('<H', len(wires))
    hdr[0x4A:0x4C] = struct.pack('<H', len(devices))

    first_id_low = devices[0].get('id_seed', 0x0DBB0000) & 0xFFFFFFFF
    hdr[0x4C:0x50] = struct.pack('<I', first_id_low)

    # ── 2. Таблиця приладів (32 B кожен) ──────────────────────────
    dev_blob = bytearray()
    for idx, d in enumerate(devices):
        did  = (d.get('id_seed', 0x97C613E9) + idx) & 0xFFFFFFFF
        dev_blob += struct.pack(
            '<II I H H f f f H H',
            did, first_id_low, 0,
            d['lib'], d.get('flags',0),
            float(d['x']), float(d['y']), float(d.get('rot',1.0)),
            d.get('pins',2), 0
        )

    # ── 3. Таблиця дротів (16 B кожен) ────────────────────────────
    wire_blob = bytearray()
    for w in wires:
        (sd,sp), (dd,dp) = w['src'], w['dst']
        bx, by = w.get('bend', (0.0,0.0))
        wire_blob += struct.pack('<H H H H f f',
                                 sd, sp, dd, dp, float(bx), float(by))

    # ── 4. П’ять нулів-«подушок» + CRC-32 ──────────────────────────
    pad5 = b'\x00'*5
    core = hdr + dev_blob + wire_blob + pad5
    crc  = zlib.crc32(core) & 0xFFFFFFFF
    return core + struct.pack('<I', crc)


# ── приклад використання ──────────────────────────────────────────
if __name__ == '__main__':
    devs = [dict(lib=0x0DBB, x=0.0, y=0.0, pins=2, flags=1)]
    wires = [dict(src=(0,2), dst=(0,1), bend=(0.5,0.0))]

    afp = build_afp(devs, wires)
    out = pathlib.Path('gen_not.AFP')
    out.write_bytes(afp)
    print(f'Створено: {out.resolve()}  ({len(afp)} байт)')
