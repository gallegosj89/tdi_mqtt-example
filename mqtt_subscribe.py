'''
script que se conecta a un broker MQTT y se subscribe a un
tópico para recibir mensajes.
'''

import random

from paho.mqtt import client as mqtt_client


# broker = 'broker.emqx.io'
# broker = 'public.mqtthq.com'
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC = "python/mqtt"
# Generate a Client ID with the subscribe prefix.
CLIENT_ID = f'subscribe-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    '''
    Función para conectar a un broker MQTT
    '''
    def on_connect(client, userdata, flags, rc, properties):
        del client, userdata, flags, properties  # Se eliminan los argumentos no utilizados
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION2,
        CLIENT_ID)
    print(f'Created client object with id {CLIENT_ID}')

    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client


def subscribe(client: mqtt_client):
    '''
    función para subscribirse a un tópico
    '''
    def on_message(client, userdata, msg):
        del client, userdata  # Se eliminan argumentos no utilizados
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(TOPIC)
    client.on_message = on_message


def run():
    '''
    Función principal dle script
    '''
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
