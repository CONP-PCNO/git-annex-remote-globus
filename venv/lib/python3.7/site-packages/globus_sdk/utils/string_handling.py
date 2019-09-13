from base64 import b64encode


def safe_b64encode(s):
    try:
        encoded = b64encode(s.encode("utf-8"))
    except UnicodeDecodeError:
        encoded = b64encode(s)

    return encoded.decode("utf-8")
