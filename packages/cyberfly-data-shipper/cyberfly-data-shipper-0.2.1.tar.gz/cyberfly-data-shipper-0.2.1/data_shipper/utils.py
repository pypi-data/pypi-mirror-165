import json
import time
from data_shipper import config
from pypact.pact import Pact

pact = Pact()


def default_meta(sender="not real"):
    return pact.lang.mk_meta(sender, config.chain_id, 0.000001, 80000, time.time().__round__()-15, 28800)


def get_api_host(network_id):
    if network_id == "testnet04":
        return "https://api.testnet.chainweb.com/chainweb/0.0/testnet04/chain/{}/pact".format(config.chain_id)
    else:
        return "https://api.chainweb.com/chainweb/0.0/mainnet01/chain/{}/pact".format(config.chain_id)


def make_rule(rule: dict) -> str:
    rule = json.loads(rule)
    variable = rule['variable']
    operator = rule['operator']
    value = rule['value']
    if not is_number(value):
        value = '"{}"'.format(value)
    return variable+' '+operator+' '+value


def publish(client, data, key_pair):
    data = json.loads(data)
    device_list = make_list(data['to_devices'])
    for device_id in device_list:
        cmd = make_cmd(data['data'], key_pair)
        try:
            mqtt_publish(client, device_id, cmd)
            print("published to device {}".format(device_id))
        except Exception as e:
            print(e.__str__())


def mqtt_publish(client, topic, cmd):
    payload = json.dumps(cmd)
    client.publish(topic, payload)


def make_cmd(data, key_pair):
    data.update({"expiry_time": time.time().__round__() + 10})
    signed = pact.crypto.sign(json.dumps(data), key_pair)
    signed.update({"device_exec": json.dumps(data)})
    return signed


def is_number(s):
    try:
        complex(s)
    except ValueError:
        return False
    return True


def make_list(s):
    if isinstance(s, list):
        return s
    return [s]
