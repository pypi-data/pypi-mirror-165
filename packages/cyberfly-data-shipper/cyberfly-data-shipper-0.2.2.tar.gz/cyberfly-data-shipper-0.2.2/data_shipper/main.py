import json

from typing import Callable
import paho.mqtt.client as mqtt
import rule_engine
from data_shipper import config, auth, api, utils

mqttc = mqtt.Client(clean_session=True)


class CyberflyDataShipper:
    def __init__(self, device_id: str, key_pair: dict, network_id: str = "mainnet01"):
        self.key_pair = key_pair
        self.network_id = network_id
        self.device_data = {}
        self.device_id = device_id
        self.account = "k:" + self.key_pair.get("publicKey")
        self.caller = default_caller
        self.mqtt_client = mqttc
        self.topic = device_id
        self.mqtt_client.user_data_set(self)
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_received
        self.run(config.mqtt_broker, config.mqtt_port)
        self.rules = []
        self.device_info = {}
        self.update_rules()
        self.update_device()

    def update_data(self, key: str, value):
        self.device_data.update({key: value})

    def on_message(self) -> Callable:
        def decorator(callback_function):
            self.caller = callback_function

        return decorator

    def run(self, host: str, port: int) -> None:
        print("trying to connect")
        try:
            self.mqtt_client.connect(host, port, 60)
        except Exception as e:
            print(e.__str__())
        try:
            self.mqtt_client.loop_start()
        except Exception as e:
            print(e.__str__())

    def process_data(self, data: dict):
        rules = self.rules
        if len(rules) == 0:
            self.update_rules()
        context = rule_engine.Context(default_value=None)
        for rule in rules:
            rul = rule_engine.Rule(utils.make_rule(rule['rule']), context=context)
            try:
                if rul.matches(data):
                    utils.publish(self.mqtt_client, rule['action'], self.key_pair)
            except Exception as e:
                print(e.__str__())

    def publish(self, topic, msg):
        signed = utils.make_cmd(msg, self.key_pair)
        utils.mqtt_publish(self.mqtt_client, topic, signed)

    def update_rules(self):
        rules = api.get_rules(self.device_id, self.network_id, self.key_pair)
        self.rules = rules

    def update_device(self):
        device = api.get_device(self.device_id, self.network_id, self.key_pair)
        self.device_info = device


def on_connect(client: mqtt.Client, mqtt_class: CyberflyDataShipper, __flags, received_code: int) -> None:
    print("Connected with result code " + str(received_code))
    client.subscribe(mqtt_class.topic)


def on_received(__client: mqtt.Client, mqtt_class: CyberflyDataShipper, msg: mqtt.MQTTMessage) -> None:
    json_string = msg.payload.decode("utf-8")
    try:
        json_data = json.loads(json_string)
        device_exec = json.loads(json_data['device_exec'])
        response_topic = device_exec.get('mqtt_response_topic')
        if auth.validate_expiry(device_exec) \
                and auth.check_auth(json_data, mqtt_class.device_info):
            try:
                if device_exec.get('update_rules'):
                    mqtt_class.update_rules()
                if device_exec.get('update_device'):
                    mqtt_class.update_device()
                mqtt_class.caller(device_exec)
                if response_topic:
                    signed = utils.make_cmd({"info": "success"}, mqtt_class.key_pair)
                    utils.mqtt_publish(__client, response_topic, signed)
            except Exception as e:
                signed = utils.make_cmd({"info": "error"}, mqtt_class.key_pair)
                utils.mqtt_publish(__client, response_topic, signed)
                print(e.__str__())
        else:
            print("auth failed")
    except Exception as e:
        print(e.__str__())


def default_caller(data):
    pass
