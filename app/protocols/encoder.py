def resp_encoder(value):
    match value:
        case int():
            return b":" + str(value).encode() + b"\r\n"
        case None:
            return b"$-1\r\n"
        case str():
            value = value.encode()
        case bytes():
            pass
    return b"$" + str(len(value)).encode() + b"\r\n" + value + b"\r\n"


def resp_array_encoder(values):
    if not values:
        return b"*0\r\n"
    encoded = b"*" + str(len(values)).encode() + b"\r\n"
    encoded += b"".join(resp_encoder(v) for v in values)
    return encoded
