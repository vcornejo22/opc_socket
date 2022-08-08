import OpenOPC
import pywintypes
import socket
import json
import time
pywintypes.datetime = pywintypes.TimeType
opc = OpenOPC.client()
opc.connect('ABB.AC800MC_OPCDaServer.3')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tagWrite = 'Applications.NTest.Test2.in'
client_socket.connect(('192.168.0.100', 10000))
try:
    listTags = ['Applications.NTest.Test2.PulseGenerator_1.Out', 'Applications.NTest.Test2.out_out']
    group = opc.read(listTags, group='test')
    while True:
        tagread = opc.read(group='test', update=1)
        tag = {tagread[0][0]: {'value': tagread[0][1], 'quality': tagread[0][2], 'timestamp': tagread[0][3]},
               tagread[1][0]: {'value': tagread[1][1], 'quality': tagread[1][2], 'timestamp': tagread[1][3]}}
        data = json.dumps(tag)
        client_socket.sendall(bytes(data, encoding='utf-8'))
        received = json.loads(client_socket.recv(1024).decode('UTF-8'))
        if received['name'] != 'Value':
            if received['value'] == 'false':
                opc.write((received['name'], False))
            elif received['value'] == 'true':
                opc.write((received['name'], True))
except OpenOPC.TimeoutError:
    pass
client_socket.close()
opc.close()

