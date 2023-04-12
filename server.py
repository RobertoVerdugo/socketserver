import socket, threading, sys

class Server ():
    
    adress = "172.31.26.59"
    port = 65436
    threads = []
    threads_users = []
    socketServer = socket.socket()
    
    def startThreads(a):
        threading.Thread(target=Server.openServer).start()

    def openServer():
        direcciones=[]
        i = 5
        Server.socketServer.bind((Server.adress, Server.port))
        while True:
            Server.socketServer.listen(i)
            i+=1
            print("Servidor abierto, esperando clientes")
            sc = Server.socketServer.accept()
            Server.threads_users.append(threading.Thread(
                target=Server.recibirUsuario, 
                args=(sc, direcciones)))
            Server.threads_users[-1].start()

    def recibirUsuario(sc, direcciones):
        direcciones.append(sc)
        data = sc[0].recv(1024)
        nombre = data.decode("utf-8")
        print(f'{nombre} ha ingresado al servidor, con ip: {sc[1][0]}')
        Server.threads.append(threading.Thread(
            target=Server.escucharMensaje, 
            args=(sc, direcciones, nombre)))
        Server.threads[-1].start()

    def escucharMensaje(sc, direcciones, nombre):
        while True:
            data = sc[0].recv(1024)
            if not data:
                break
            data = nombre + ": " + data.decode("utf-8")
            print(data)
            for direccion in direcciones:
                direccion[0].send(data.encode())


servidor = Server()
servidor.startThreads()
