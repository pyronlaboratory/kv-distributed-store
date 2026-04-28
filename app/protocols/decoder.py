def resp_decoder(data):
    args = data.split(b"\r\n")
    it = iter(args)
    length = int(next(it)[1:])  # *N
    return [next(it) for _ in (next(it) for _ in range(length))]  # skip $N, yield value
