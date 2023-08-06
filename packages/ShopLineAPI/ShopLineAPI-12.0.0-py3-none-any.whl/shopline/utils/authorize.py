import hashlib
import hmac
import base64
import json
import time


def hmac_sha256(source, secret):
    assert source, "source is None"
    assert secret, "secret is None"
    signature = hmac.new(secret.encode("utf-8"), source.encode("utf-8"), digestmod=hashlib.sha256).hexdigest()
    return signature


def get_sign(secret, timestamp, **data):

    source = "{}{}".format(parse_body(**data), timestamp)
    return hmac_sha256(source, secret)


def get_sign1(secret, timestamp, cd):
    d1 = '{\\"code\\":\\"' + cd + '\\"}'

    source = "{}{}".format(d1, timestamp)
    return hmac_sha256(source, secret)


def parse_get_url(**param):
    return "&".join(["{}={}".format(k, v) for k, v in param.items()])


def parse_body(**data):
    if data is None or len(data) == 0:
        return ""

    ps = ",".join(['"{}":"{}"'.format(k, v) for k, v in data.items()])
    return "{" + ps + "}"

def parse_json_data(**data):
    return parse_body(**data).encode()


def authorize_get_sign(secret, **param):
    """get method get param"""
    assert param['appkey'], "GET [missing appKey]"
    assert param['timestamp'], "GET [missing timestamp]"
    source = parse_get_url(**param)
    return hmac_sha256(source, secret)

def get_timestamp():
    return str(int(time.time()*1000))
if __name__ == '__main__':
    # hmac_sha256("1","None")
    parse_body()
