FROM python:3.13-slim

WORKDIR /app

COPY server.py .

EXPOSE 50001

CMD ["python", "-u", "server.py"]
# -u flag para imprimir em tempo real nos logs e console