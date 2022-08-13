import OpenOPC, pywintypes, socket, json, threading

pywintypes.datetime = pywintypes.TimeType
listTags = ['Applications.NTest.Test2.PulseGenerator_1.Out', 'Applications.NTest.Test2.out_out', 'Applications.NTest.Test1_1.Mot1_1.IO.In.EnSeqStart', 'Applications.NTest.Test1_1.Mot1_1.IO.In.EnSeqStop',
                'Applications.NTest.Test1_1.Mot1_1.IO.In.IA', 'Applications.NTest.Test1_1.Mot1_1.IO.In.IB1',
                'Applications.NTest.Test1_1.Mot1_1.IO.In.IB2', 'Applications.NTest.Test1_1.Mot1_1.IO.In.IB3',
                'Applications.NTest.Test1_1.Mot1_1.IO.In.IB4', 'Applications.NTest.Test1_1.Mot1_1.IO.In.IC',
                'Applications.NTest.Test1_1.Mot1_1.IO.In.Warning', 'Applications.NTest.Test1_1.Mot1_2.IO.In.EnSeqStart',
                'Applications.NTest.Test1_1.Mot1_2.IO.In.EnSeqStop', 'Applications.NTest.Test1_1.Mot1_2.IO.In.IA',
                'Applications.NTest.Test1_1.Mot1_2.IO.In.IB1', 'Applications.NTest.Test1_1.Mot1_2.IO.In.IB2',
                'Applications.NTest.Test1_1.Mot1_2.IO.In.IB3', 'Applications.NTest.Test1_1.Mot1_2.IO.In.IB4',
                'Applications.NTest.Test1_1.Mot1_2.IO.In.IC', 'Applications.NTest.Test1_1.Mot1_2.IO.In.Warning',
                'Applications.NTest.Test1_1.TP_1.ET', 'Applications.NTest.Test1_1.TP_1.In', 'Applications.NTest.Test1_1.TP_1.PT',
                'Applications.NTest.Test1_1.TP_1.Q', 'Applications.NTest.Test1_1.TP_2.ET',
                'Applications.NTest.Test1_1.TP_2.In', 'Applications.NTest.Test1_1.TP_2.PT',
                'Applications.NTest.Test1_1.TP_2.Q', 'Applications.NTest.Test1_1.PulseGenerator_1.Enable',
                'Applications.NTest.Test1_1.PulseGenerator_1.EnableParError', 'Applications.NTest.Test1_1.PulseGenerator_1.Out',
                'Applications.NTest.Test1_1.PulseGenerator_1.ParError', 'Applications.NTest.Test1_1.PulseGenerator_1.PeriodTime',
                'Applications.NTest.Test1_1.PulseGenerator_1.PulseTime', 'Applications.NTest.Test1_1.PulseGenerator_2.Enable',
                'Applications.NTest.Test1_1.PulseGenerator_2.EnableParError', 'Applications.NTest.Test1_1.PulseGenerator_2.Out',
                'Applications.NTest.Test1_1.PulseGenerator_2.ParError', 'Applications.NTest.Test1_1.PulseGenerator_2.PeriodTime',
                'Applications.NTest.Test1_1.PulseGenerator_2.PulseTime']

class thread_client(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket

    def run(self):
        opc = OpenOPC.client()
        opc.connect('ABB.AC800MC_OPCDaServer.3')
        #value = False
        tagWrite = 'Applications.NTest.Test2.in'
        while True:
            try:
                received = json.loads(self.client_socket.recv(1024).decode('UTF-8'))
                if received['value'] == 'false':
                    opc.write((tagWrite, False))
                elif received['value'] == 'true':
                    opc.write((tagWrite, True))
            except OpenOPC.OPCError:
                pass
def main():
    opc = OpenOPC.client()
    opc.connect('ABB.AC800MC_OPCDaServer.3')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.0.100', 10000))
    thread = thread_client(client_socket)
    thread.start()
    while True:
        try:
            tagread = opc.read(listTags, group='test')
            tag = {}
            for i in range(len(tagread)):
                tag1 = {tagread[i][0]: {'value': tagread[i][1]}}
                tag.update(tag1)
            data = json.dumps(tag)
            #print(data)
            client_socket.sendall(bytes(data, encoding='utf-8'))
            #time.sleep(5)
        except OpenOPC.TimeoutError:
            pass
    client_socket.close()
    opc.close()

if __name__ == '__main__':
    main()
