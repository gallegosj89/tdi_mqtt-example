'''
Chat que utiliza el protocolo MQTT, envía mensajes comunes a un topic publico,
y también es capaz de enviar mensajes  topics privados. Se subscribe para escuchar
mensajes de el topic público y también está subscrito a su propio topic privado.
'''

# import random
import signal
import sys

from paho.mqtt import client as mqtt_client


# broker = 'broker.emqx.io'  # https://www.emqx.com/en/mqtt/public-mqtt5-broker
MATRICULA = '317944'
BROKER = 'broker.hivemq.com'
PORT = 1883
HEADER = "topic/tdi/2025-1/"
PUBLIC_TOPIC = f"{HEADER}public"
PRIVATE_TOPIC = f"{HEADER}{MATRICULA}"

# Generate a Client ID with the publish prefix.
# client_id = f'publish-{random.randint(0, 1000)}'
CLIENT_ID = f'##{MATRICULA}'
# username = 'emqx'
# password = 'public'


def connect_mqtt():
    '''
    Función para conectarse a un broker MQTT
    '''
    def on_connect(client, userdata, flags, rc, properties):
        del client, userdata, flags, properties  # Se eliminan los argumentos no utilizados
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION2,
        CLIENT_ID
    )
    print(f'Created client object with id {CLIENT_ID}')

    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client


def publish(client):
    '''
    función para publicar un mensaje MQTT
    '''
    while True:
        msg = input('')
        topic = ''
        if msg[0] == '#' and msg[1] == '#':
            msg_list = msg.split('##')
            print(len(msg_list))
            print(msg_list)
            if len(msg_list) <= 2:
                print('\nPrivate message not sent\n \
                      Try ##<Client ID>##<Message>\n \
                      E.g. ##317944##Hello world!\n')
                continue
            topic = f'{HEADER}{msg_list[1]}'
            msg = msg_list[2]
        else:
            topic = PUBLIC_TOPIC

        print(f"Sending `{msg}` to topic `{topic}`")

        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


def subscribe(client: mqtt_client):
    '''
    Función para subscribirse a un topic
    '''
    def on_message(client, userdata, msg):
        del client, userdata  # Se eliminan los argumentos no utilizados
        print(f"Received from topic `{msg.topic}`\n\t> {msg.payload.decode()}")

    client.subscribe(PUBLIC_TOPIC)
    client.subscribe(PRIVATE_TOPIC)

    client.on_message = on_message


def run():
    '''
    Función principal del script
    '''
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    def on_signal(sig, frame):
        '''
        Función para recibir la interrupción de teclado
        '''
        del sig, frame  # eliminar argumentos no utilizados
        print('\n\nYou pressed Ctrl+C!')
        sys.exit(0)

    # Register signal handler
    signal.signal(signal.SIGINT, on_signal)

    # Run bussines logic
    run()
