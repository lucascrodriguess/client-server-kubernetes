from socket import *
import signal
import sys
import threading
from datetime import datetime
import csv
import os

csv_lock = threading.Lock()

def signal_handler(sig, frame):
    print("Servidor encerrado.")
    s.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

host = '0.0.0.0'
port = 50001

s = socket(AF_INET, SOCK_STREAM)
s.bind((host, port))
s.listen()
print(f"Servidor escutando em {host}:{port}...")

hostname = gethostname()
ip = gethostbyname(hostname)
print(f"IP do servidor: {ip}")


def log_to_csv(addr, message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-2]  # até milissegundos
    with csv_lock:
        with open('log_clients.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([now, addr[0], addr[1], message])
            csvfile.flush()  # Força escrita imediata no disco
            os.fsync(csvfile.fileno())  # Força sincronização com o sistema de arquivos


def handle_client(conn, addr):
    print(f"Conectado por {addr}")
    with conn:
        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                print(f"Conexão fechada por {addr}")
                break

            mensagens = msg.strip().split('\n')
            for m in mensagens:
                if m:
                    print(f"Mensagem do cliente {addr}: {m}")
                    log_to_csv(addr, m)

while True:
    try:
        conn, addr = s.accept()
        print(f"Conexão recebida de: {addr}")

        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.daemon = True
        client_thread.start()

    except KeyboardInterrupt:
        print ("Fechando o servidor...")
        s.close()