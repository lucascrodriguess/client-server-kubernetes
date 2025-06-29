package main

import (
	"flag"
	"fmt"
	"log"
	"net"
	//"strconv"
)

func main() {
	// Definir flags de linha de comando
	host := flag.String("host", "172.17.0.2", "Endereço do servidor")
	port := flag.Int("port", 50001, "Porta do servidor")
	messages := flag.Int("messages", 1, "Número de mensagens a enviar")
	flag.Parse()
	
	address := fmt.Sprintf("%s:%d", *host, *port)
	
	// Conectar ao servidor
	conn, err := net.Dial("tcp", address)
	if err != nil {
		log.Fatalf("Erro ao conectar: %v", err)
	}
	defer conn.Close()
	
	fmt.Printf("Conectado ao servidor %s!\n", address)
	
	// Obter endereço local
	localAddr := conn.LocalAddr().String()
	localHost, localPort, _ := net.SplitHostPort(localAddr)
	
	// Enviar mensagens
	for i := 0; i < *messages; i++ {
		message := fmt.Sprintf("%d %s:%s", i+1, localHost, localPort)
		
		_, err := fmt.Fprintf(conn, "%s\n", message)
		if err != nil {
			log.Printf("Erro ao enviar: %v", err)
			break
		}
		
		fmt.Printf("Enviada: %s\n", message)
	}
	
	fmt.Println("Finalizando conexão...")
}
