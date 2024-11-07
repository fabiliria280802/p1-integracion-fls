from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import signal

authorizer = DummyAuthorizer()
authorizer.add_user("fabiliria", "773H", r"C:\Users\PC\Desktop\ftp", perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer

address = ("172.31.83.27", 21)
server = FTPServer(address, handler)

def signal_handler(signal, frame):
    print("Servidor detenido.")
    server.close_all()

signal.signal(signal.SIGINT, signal_handler)

print("Servidor FTP iniciado. Presiona Ctrl+C para detenerlo.")
server.serve_forever()
