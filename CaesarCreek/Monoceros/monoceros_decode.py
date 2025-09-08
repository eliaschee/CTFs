# monoceros_decode.py
# Re-implementation of the decoded logic from the embedded decoder binary.

def FUN_001011f5(param_1: int) -> int:
    # Range check; returns left-shifted value on success.
    if param_1 < 0 or 0x10000 < param_1:
        return -0xFE
    return param_1 << 2

def FUN_00100d40(param_1: bytearray, param_2: int, param_3: bytearray, param_4: int) -> int:
    # Core unpacking routine (base-0x55 style) translated from decompiled C.
    local_18 = FUN_001011f5(param_2)
    if local_18 < 0:
        return local_18

    if param_4 < local_18:
        return -0xFF

    local_14 = 0
    local_18 = 0
    while local_14 < param_2:
        local_c = param_2 - local_14
        if param_1[local_14] == ord('z'):
            local_14 += 1
            local_10 = 0
            local_c = 5
        else:
            # Character range validation (printable subset used by the encoding).
            c = param_1[local_14]
            cVar1 = 1 if (c < 0x21 or 0x75 < c) else 0
            if any(cVar1 != 0 for _ in range(5 if local_c < 5 else local_c)):
                return -0xFD

            if local_c < 5:
                iVar5 = local_14 + 1
                lVar7 = local_14
                if iVar5 < param_2:
                    iVar4 = param_1[iVar5] - 0x21
                    local_14 += 2
                else:
                    iVar4 = 0x54
                    local_14 = iVar5

                if local_14 < param_2:
                    iVar5 = param_1[local_14] - 0x21
                    local_14 += 1
                else:
                    iVar5 = 0x54

                if local_14 < param_2:
                    iVar6 = param_1[local_14] - 0x21
                    local_14 += 1
                else:
                    iVar6 = 0x54

                uVar3 = ((((param_1[lVar7] - 0x21) * 0x55 + iVar4) * 0x55 + iVar5) * 0x55 + iVar6)
                if uVar3 > 0x3030303:
                    return -0xFC

                if local_14 < param_2:
                    bVar2 = param_1[local_14] - 0x21
                    local_14 += 1
                else:
                    bVar2 = 0x54

                uVar3 = uVar3 * 0x55
                if bVar2 > uVar3:
                    return -0xFC

                local_10 = uVar3 + bVar2
            else:
                iVar5 = local_14 + 4
                uVar3 = ((((param_1[local_14] - 0x21) * 0x55 +
                           (param_1[local_14 + 1] - 0x21)) * 0x55 +
                          (param_1[local_14 + 2] - 0x21)) * 0x55 +
                         (param_1[local_14 + 3] - 0x21))

                if uVar3 > 0x3030303:
                    return -0xFC

                local_14 += 5
                bVar2 = param_1[iVar5] - 0x21
                uVar3 = uVar3 * 0x55

                if bVar2 > uVar3:
                    return -0xFC

                local_10 = uVar3 + bVar2

        # Write 32-bit chunk big-endian
        param_3[local_18 + 3] = local_10 & 0xFF
        param_3[local_18 + 2] = (local_10 >> 8) & 0xFF
        param_3[local_18 + 1] = (local_10 >> 16) & 0xFF
        param_3[local_18 + 0] = (local_10 >> 24) & 0xFF

        local_18 += (local_c - 1) if local_c < 5 else 4

    return local_18

def FUN_0010081a(buf: bytearray) -> str:
    # Step 1: XOR with 0x0F
    for i in range(len(buf)):
        buf[i] ^= 0x0F

    # Step 2: compute output size and unpack
    sVar2 = len(buf)
    uVar1 = FUN_001011f5(sVar2 & 0xFFFFFFFF)

    decoded = bytearray(sVar2)
    FUN_00100d40(buf, sVar2 & 0xFFFFFFFF, decoded, uVar1)

    # Keep printable bytes; strip trailing newline if present
    out = "".join(chr(b) for b in decoded if 32 <= b < 127)
    return out.rstrip()

def FUN_001008ae() -> None:
    # Encoded input string (from the challenge)
    input_bytes = (b"N`'bhGX#+ N7#Z}0U[a.HO#^%O3\"'-M;,$QIKVG\"LAJfbO4RIlN\\l3bJ#`A:N\\z[|IK#:bI&U =O5XPoNbR*kK nX1N[K!+McS04N[A7")
    buf = bytearray(input_bytes)
    print(FUN_0010081a(buf))

if __name__ == '__main__':
    FUN_001008ae()
