import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8001))
server.listen()
sock, addr = server.accept()

data = sock.recv(1024)
print(data.decode("utf8"))
sock.close()
server.close()
