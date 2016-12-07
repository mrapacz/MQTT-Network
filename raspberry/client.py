import paho.mqtt.client as mqtt
import config
import json
from weatherserver.utils.dumper import dump_data

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for node in config.node_ids:
        client.subscribe("nodemcu/" + node)



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(message)
    json_msg = json.loads(message)
    print(json_msg)
    dump_data(json_msg['id'], json_msg['temperature'])
    

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(config.host, config.port, 60)
    client.loop_forever()
