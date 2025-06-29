.PHONY: build-server build-client build-all run-server run-client docker-build-server docker-build-client docker-build-all clean

# Compilar binários
build-server:
	go build -o bin/server server/server.go

build-client:
	go build -o bin/client client/client.go

build-all: build-server build-client

# Executar localmente
run-server: build-server
	./bin/server

run-client: build-client
	./bin/client --host localhost --port 50001 --messages 5

# Construir imagens Docker
docker-build-server:
	docker build -f server/Dockerfile -t tcp_server_go .

docker-build-client:
	docker build -f client/Dockerfile -t tcp_client_go .

docker-build-all: docker-build-server docker-build-client

# Executar com Docker
docker-run-server:
	docker run --rm -p 50001:50001 tcp_server_go

docker-run-client:
	docker run --rm tcp_client_go ./client --messages 10
#	docker run --rm tcp_client_go ./client --host host.docker.internal --port 50001 --messages 10

# Deploy no Kubernetes
k8s-deploy:
	kubectl apply -f server/deployment.yaml
	kubectl apply -f client/job.yaml

k8s-clean:
	kubectl delete -f server/deployment.yaml
	kubectl delete -f client/job.yaml

# Limpeza
clean:
	rm -rf bin/
	rm -f log_clients.csv
