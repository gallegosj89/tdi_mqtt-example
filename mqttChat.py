# import random
import signal
import sys

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'  # https://www.emqx.com/en/mqtt/public-mqtt5-broker
port = 1883
publicTopic = "topic/tdi/2024-1/public"
privateTopic = "topic/tdi/2024-1/317944"
privateHeader = "topic/tdi/2024-1/"
# Generate a Client ID with the publish prefix.
# client_id = f'publish-{random.randint(0, 1000)}'
client_id = '##317944'
# username = 'emqx'
# password = 'public'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc, prefences):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION2,
        client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    # msg_count = 1
    while True:
        # time.sleep(1)
        # msg = f"messages: {msg_count}"
        msg = input('')
        topic = ''
        if msg[0] == '#' and msg[1] == '#':
            msgList = msg.split('##')
            print(len(msgList))
            print(msgList)
            if len(msgList) <= 2:
                print('\nPrivate message not sent\n \
                      Try ##<Client ID>##<Message>\n \
                      E.g. ##317944##Hello world!\n')
                continue
            topic = f'{privateHeader}{msgList[1]}'
            msg = msgList[2]
        else:
            topic = publicTopic
        print(f"Sending `{msg}` to topic `{topic}`")
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        # msg_count += 1
        # if msg_count > 5:
        #    break


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received from `{client._client_id.decode().split('##')[1]}` on topic `{msg.topic}`\n\t> {msg.payload.decode()}")

    client.subscribe(publicTopic)
    client.subscribe(privateTopic)

    client.on_message = on_message


def run():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)
    publish(client)
    client.loop_stop()


def signal_handler(sig, frame):
    print('\n\nYou pressed Ctrl+C!')
    sys.exit(0)


if __name__ == '__main__':
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Run bussines logic
    run()
