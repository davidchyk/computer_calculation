# afp_build.py  –  сформувати AFDK-2.0 .AFP

import struct, zlib, time, pathlib

HDR_LEN   = 0x50      # 80 B
DEV_SIZE  = 32        # payload без рамок
WIRE_SIZE = 30        # 16 B core + 14 B pad

# ──────────── SERVICE ──────────────────────────────────────────────
def ts64():                       # 64-bit μs timestamp → 8 B LE
    return int(time.time()*1_000_000).to_bytes(8, 'little')

def crc32(data: bytes) -> bytes:  # CRC-32 LE
    return struct.pack('<I', zlib.crc32(data) & 0xFFFFFFFF)

# ──────────── MAIN BUILDER ─────────────────────────────────────────
def build_afp(devices, wires, grid=1, first_id=0x01000000):
    """
    devices: [{lib:0x1B0D, pins:3, x:-2.0, y:0.0, rot:1.0, flags:0}, …]
    wires:   [{src:(0,1), dst:(1,2), bend:(0.0,0.0)}, …]
    """

    # 1. ── Header 80 B ─────────────────────────────────────────────
    hdr = bytearray(HDR_LEN)
    hdr[0:8]   = ts64()
    hdr[8:12]  = b'\x40\x00\x04\x00'      # постійна сигнатура
    hdr[0x42:0x44] = struct.pack('<H', grid)
    hdr[0x46:0x48] = struct.pack('<H', len(wires))
    hdr[0x4A:0x4C] = struct.pack('<H', len(devices))
    hdr[0x4C:0x50] = struct.pack('<I', first_id & 0xFFFFFFFF)

    # 2. ── Device-payloads (32 B кожен) ───────────────────────────
    dev_blob = bytearray()
    for idx, d in enumerate(devices):
        did = first_id + idx          # унікальний ID
        dev_blob += struct.pack(
            '<II I H H f f f H H',
            did,                      # id
            first_id & 0xFFFFFFFF,    # guid копія
            0,                        # zero
            d['lib'], d.get('flags',0),
            float(d['x']), float(d['y']), float(d.get('rot',1.0)),
            d.get('pins',2), 0
        )

    # 3. ── Wire-payloads (30 B) ───────────────────────────────────
    wire_blob = bytearray()
    for w in wires:
        (sd,sp), (dd,dp) = w['src'], w['dst']
        bx, by = w.get('bend',(0.0,0.0))
        wire_blob += struct.pack('<H H H H f f', sd,sp, dd,dp, bx,by)
        wire_blob += b'\x00'*14       # паддинг, як в еталонах

    # 4. ── Tail: 5 нулів + CRC-32 ─────────────────────────────────
    body = hdr + dev_blob + wire_blob + (b'\x00'*5)
    full = body + crc32(body)
    return full

# ──────────── ПРИКЛАД: схематичка X,Y→AND→Z→AND→N ────────────────
if __name__ == '__main__':
    LIB_VAR  = 0x0101
    LIB_AND2 = 0x1B0D     # 2-вхідний AND

    devices = [
        dict(lib=LIB_VAR , pins=1, x=-4, y= 1),       # 0  X
        dict(lib=LIB_VAR , pins=1, x=-4, y=-1),       # 1  Y
        dict(lib=LIB_AND2, pins=3, x=-2, y= 0),       # 2  AND1
        dict(lib=LIB_VAR , pins=1, x= 0, y=-1),       # 3  Z
        dict(lib=LIB_AND2, pins=3, x= 2, y= 0),       # 4  AND2
        dict(lib=LIB_VAR , pins=1, x= 4, y= 0),       # 5  N
    ]

    def w(sdev, spin, ddev, dpin):
        return dict(src=(sdev,spin), dst=(ddev,dpin), bend=(0.0,0.0))

    wires = [
        w(0,1, 2,1),      # X → AND1.in1
        w(1,1, 2,2),      # Y → AND1.in2
        w(2,3, 4,1),      # AND1.out → AND2.in1
        w(3,1, 4,2),      # Z → AND2.in2
        w(4,3, 5,1),      # AND2.out → N
    ]

    afp_bytes = build_afp(devices, wires)
    outfile = pathlib.Path('xy_and_chain.AFP')
    outfile.write_bytes(afp_bytes)
    print(f'Готово → {outfile.resolve()}  ({len(afp_bytes)} B)')
