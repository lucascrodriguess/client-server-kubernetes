package main

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"log"
	"net"
	"os"
	"os/signal"
	"strings"
	"sync"
	"syscall"
	"time"
)

var (
	csvMutex sync.Mutex
	csvFile  *os.File
	csvWriter *csv.Writer
)

func initCSV() error {
	var err error
	csvFile, err = os.OpenFile("log_clients.csv", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err != nil {
		return err
	}
	csvWriter = csv.NewWriter(csvFile)
	return nil
}

func closeCSV() {
	if csvWriter != nil {
		csvWriter.Flush()
	}
	if csvFile != nil {
		csvFile.Close()
	}
}

func logToCSV(addr net.Addr, message string) {
	now := time.Now().Format("2006-01-02 15:04:05.000")
	
	// Extrair IP e porta do endereço
	host, port, _ := net.SplitHostPort(addr.String())
	
	csvMutex.Lock()
	defer csvMutex.Unlock()
	
	record := []string{now, host, port, message}
	if err := csvWriter.Write(record); err != nil {
		log.Printf("Erro ao escrever no CSV: %v", err)
		return
	}
	csvWriter.Flush()
	
	// Força sincronização com o disco
	if err := csvFile.Sync(); err != nil {
		log.Printf("Erro ao sincronizar arquivo: %v", err)
	}
}

func handleClient(conn net.Conn) {
	defer conn.Close()
	
	addr := conn.RemoteAddr()
	fmt.Printf("Conectado por %s\n", addr)
	
	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		message := strings.TrimSpace(scanner.Text())
		if message == "" {
			continue
		}
		
		fmt.Printf("Mensagem do cliente %s: %s\n", addr, message)
		logToCSV(addr, message)
	}
	
	if err := scanner.Err(); err != nil {
		log.Printf("Erro ao ler do cliente %s: %v", addr, err)
	}
	
	fmt.Printf("Conexão fechada por %s\n", addr)
}

func main() {
	// Inicializar arquivo CSV
	if err := initCSV(); err != nil {
		log.Fatalf("Erro ao inicializar CSV: %v", err)
	}
	defer closeCSV()
	
	// Configurar tratamento de sinais
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	
	host := "0.0.0.0"
	port := "50001"
	address := fmt.Sprintf("%s:%s", host, port)
	
	// Criar listener
	listener, err := net.Listen("tcp", address)
	if err != nil {
		log.Fatalf("Erro ao criar listener: %v", err)
	}
	defer listener.Close()
	
	fmt.Printf("Servidor escutando em %s...\n", address)
	
	// Obter e exibir IP do servidor
	hostname, err := os.Hostname()
	if err == nil {
		if addrs, err := net.LookupHost(hostname); err == nil && len(addrs) > 0 {
			fmt.Printf("IP do servidor: %s\n", addrs[0])
		}
	}
	
	// Goroutine para tratamento de sinais
	go func() {
		<-sigChan
		fmt.Println("\nServidor encerrado.")
		listener.Close()
		os.Exit(0)
	}()
	
	// Loop principal para aceitar conexões
	for {
		conn, err := listener.Accept()
		if err != nil {
			// Verifica se o erro é devido ao fechamento do listener
			if opErr, ok := err.(*net.OpError); ok && opErr.Err.Error() == "use of closed network connection" {
				break
			}
			log.Printf("Erro ao aceitar conexão: %v", err)
			continue
		}
		
		fmt.Printf("Conexão recebida de: %s\n", conn.RemoteAddr())
		
		// Iniciar goroutine para tratar o cliente
		go handleClient(conn)
	}
}
