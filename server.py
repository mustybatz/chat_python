import socket
import pickle
import sys
import threading

class Servidor():
    def __init__(self, host = "148.201.188.178", port="4000"):

        self.clientes = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)

        #hilos para aceptar y rechazar conexiones.
        aceptar = threading.Thread(target=self.aceptarCon)
        procesar = threading.Thread(target=self.procesarCon)

        aceptar.daemon = True
        aceptar.start()

        procesar.daemon = True
        procesar.start()

        try:
            while True:
                msg = input(">")
                if msg == "Bye":
                    break
            self.sock.close()
            sys.exit()
        except:
            self.sock.close()
            sys.exit()
    #función para mostrar mensajes
    def msg_to_all(self, msg, cliente):
        for c in self.clientes:
            try:
                if c != cliente:
                    c.send(msg)
            except:
                self.clientes.remove(c)
    #función que acepta las conexiones y las almacena en un arreglo
    def aceptarCon(self):
        print("Aceptar conexión iniciado.")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clientes.append(conn)
            except:
                pass
    #función que procesa las conexiones.
    def procesarCon(self):
        print("Procesar conexión iniciado.")
        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(1024)
                        if data:
                            self.msg_to_all(data,c)
                    except:
                        pass 

#Iniciar servidor.
c = Servidor()
