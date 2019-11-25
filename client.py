import socket
import sys
import pickle
import threading

class Cliente():

    def __init__(self, host="148.201.188.178", port=4000):
        #conexión del cliente al servidor
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))
        #Leer mensajes del servidor mediante un hilo
        msg_recv = threading.Thread(target=self.msg_recv)

        msg_recv.daemon = True
        msg_recv.start()

        #Hilo que mantendrá vivo el hilo principal y nos permitirá escribir los mensajes.
        while True:
            msg = input('>')
            if msg != 'Bye':
                self.send_msg(msg)
            else:
                self.sock.close()
                sys.exit()
    #Función para recibir mensajes
    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    print(f">{pickle.loads(data)}")
            except:
                pass
    #Función para mandar mensajes
    def send_msg(self, msg):
        try:
            self.sock.send(pickle.dumps(msg))
        except:
            print("error")

c = Cliente()
