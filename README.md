# TCP Server/Client em Go

Este projeto é uma conversão do servidor e cliente TCP originalmente escritos em Python para a linguagem Go.

## Funcionalidades

### Servidor (`server.go`)
- Escuta conexões TCP na porta 50001
- Suporta múltiplas conexões simultâneas usando goroutines
- Registra todas as mensagens recebidas em um arquivo CSV (`log_clients.csv`)
- Tratamento gracioso de sinais (SIGINT, SIGTERM)
- Thread-safe para escrita no arquivo CSV

### Cliente (`client.go`)
- Conecta ao servidor TCP
- Envia um número configurável de mensagens
- Suporte a argumentos de linha de comando

## Como usar

### Compilação
\`\`\`bash
# Compilar ambos
make build-all

# Ou individualmente
make build-server
make build-client
\`\`\`

### Execução local
\`\`\`bash
# Terminal 1 - Servidor
make run-server

# Terminal 2 - Cliente
make run-client
# ou com parâmetros customizados
./bin/client --host localhost --port 50001 --messages 10
\`\`\`

### Docker
\`\`\`bash
# Construir imagens
make docker-build-all

# Executar servidor
make docker-run-server

# Executar cliente
make docker-run-client
\`\`\`

### Kubernetes
\`\`\`bash
# Deploy
make k8s-deploy

# Limpar
make k8s-clean
\`\`\`

## Argumentos do Cliente

- `--host`: Endereço do servidor (padrão: 172.17.0.2)
- `--port`: Porta do servidor (padrão: 50001)
- `--messages`: Número de mensagens a enviar (padrão: 1)

## Arquivo de Log

O servidor cria um arquivo `log_clients.csv` com o formato:
\`\`\`
timestamp,ip,port,message
\`\`\`

## Diferenças da versão Python

1. **Goroutines** em vez de threads Python
2. **Flags** nativas do Go para argumentos de linha de comando
3. **Mutex** para sincronização thread-safe
4. **Bufio.Scanner** para leitura eficiente de linhas
5. **Tratamento de sinais** usando channels do Go
