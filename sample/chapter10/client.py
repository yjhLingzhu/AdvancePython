import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8001))
client.send("yjh".encode("utf8"))
client.close()
