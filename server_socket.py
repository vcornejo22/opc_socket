import socket, json, threading, time
import paho.mqtt.client as mqtt

msg_payload = 0
msg_topic = ''
host = '192.168.0.100'
port_socket = 10000
port_mqtt = 1883

def on_connect(client, useData, flags, rc):
    if rc==0:
        print('Client is connected')
        global connected
    else:
        print('Connection failed')
        
def on_message(client, userdata ,message):
    global msg_payload
    global msg_topic
    # print(str(message.payload.decode('utf-8')), message.topic)
    msg_payload = (message.payload.decode('utf-8'))
    msg_topic = message.topic
    
class thread_server(threading.Thread):
    def __init__(self, conn, address, client_mqtt):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address
        self.client_mqtt = client_mqtt
        
    def run(self):
         while True:
            self.client_mqtt.loop_start()
            self.client_mqtt.subscribe('Applications.NTest.Test2.in')
            self.client_mqtt.loop_stop() 
            if msg_payload != 0:
                message_json = json.dumps({'topic': msg_topic, 'value': msg_payload})
                self.conn.sendall(bytes(message_json, encoding='utf-8'))
            time.sleep(1)
def main():
    # Configuration server socker
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port_socket))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print(f'Connection from: {str(address)}')
    # Configuration client mqtt
    client_mqtt = mqtt.Client()
    client_mqtt.on_message = on_message
    client_mqtt.on_connect = on_connect
    client_mqtt.connect(host, port=port_mqtt)
    path = 'Applications.NTest.Test1_1.PulseGenerator_1.Enable'
    thread = thread_server(conn, address, client_mqtt)
    thread.start()
    while True:
        message_socket = conn.recv(4096).decode('utf-8')
        if message_socket:
            client_mqtt.publish('server', message_socket)
            # print(message_socket)
   
    conn.close()
if __name__ == '__main__':
    main()