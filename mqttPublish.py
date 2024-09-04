from paho.mqtt import client as mqtt_client
import random
import time


# broker = 'broker.emqx.io'
broker = 'public.mqtthq.com'
port = 1883
topic = 'python/mqtt'
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print('Connected to MQTT Broker!')
        else:
            print('failed to connect, return code %d\n', rc)
    # Set connecting client ID
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id)
    # client.usename_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


# FIRST_RECONNECT_DELAY = 1
# RECONNECT_RATE = 2
# MAX_RECONNECT_COUNT = 12
# MAX_RECONNECT_DELAY = 60

# def on_disconnect(client, userdata, rc):


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message `{msg}` to topic `{topic}`")
        msg_count += 1
        if msg_count > 5:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
