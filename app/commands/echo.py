from app.protocols.encoder import resp_encoder


def execute(args):
    return resp_encoder(args[1])
