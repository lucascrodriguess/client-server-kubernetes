from socket import *
import argparse

parser = argparse.ArgumentParser(description="Cliente TCP configurável")
parser.add_argument('--host', type=str, default='172.17.0.2', help='Endereço do servidor')
parser.add_argument('--port', type=int, default=50001, help='Porta do servidor')
parser.add_argument('--messages', type=int, default=1, help='Número de mensagens a enviar')

args = parser.parse_args()

c = socket(AF_INET, SOCK_STREAM)

try:
    c.connect((args.host, args.port))
    print(f"Conectado ao servidor {args.host}:{args.port}!")

except Exception as e:
    print(f"Erro ao conectar: {e}")
    exit()

for i in range(args.messages):
    try:
        msg = f"{i+1} {c.getsockname()[0]}:{c.getsockname()[1]}"
        c.send((msg + "\n").encode())
        print(f"Enviada: {msg}")

    except Exception as e:
        print(f"Erro ao enviar: {e}")
        break

print("Finalizando conexão...")
c.close()