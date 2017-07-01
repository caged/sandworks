

def hex_to_rgb_decimal(hex):
    return [v / 255 for v in list(bytes.fromhex(hex))]
