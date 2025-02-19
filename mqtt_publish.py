'''
Este script se conecta a un broker MQTT y envía mensajes
publicandolos a ese broker.
'''

import random
import time

from paho.mqtt import client as mqtt_client


# broker = 'broker.emqx.io'
# broker = 'public.mqtthq.com'
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC = 'python/mqtt'
CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt():
    '''
    Función para conectar el cliente con el broker
    '''
    def on_connect(client, userdata, flags, rc, properties):
        del client, userdata, flags, properties  # Se eliminan los argumentos no utilizados
        if rc == 0:
            print('Connected to MQTT Broker!')
        else:
            print('failed to connect, return code %d\n', rc)

    # Set connecting client ID
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, CLIENT_ID)
    print(f'Created client object with id {CLIENT_ID}')

    # client.usename_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client


# FIRST_RECONNECT_DELAY = 1
# RECONNECT_RATE = 2
# MAX_RECONNECT_COUNT = 12
# MAX_RECONNECT_DELAY = 60

# def on_disconnect(client, userdata, rc):


def publish(client):
    '''
    función que publica una cantidad finita de mensajes
    '''
    msg_count = 1
    while True:
        time.sleep(1)

        msg = f"messages: {msg_count} diferente"
        result = client.publish(TOPIC, msg)

        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{TOPIC}`")
        else:
            print(f"Failed to send message `{msg}` to topic `{TOPIC}`")

        msg_count += 1
        if msg_count > 5:
            break


def run():
    '''
    Función principal del script
    '''
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
