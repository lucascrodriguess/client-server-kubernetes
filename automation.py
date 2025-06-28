import os
import yaml
import time
import csv
from graph import gerar_graficos

server_counts = [2, 6, 10]
client_counts = [10, 40, 70, 100]
message_counts = [1, 10, 100] 

def unir_csv(csv_arquivos, servers, clients, messages):
  arquivo_saida = f"./csv/{servers}_{clients}_{messages}.csv"

  with open(arquivo_saida, "w", newline="") as saida:
      escritor = csv.writer(saida)

      for i, arquivo in enumerate(csv_arquivos):
          with open(arquivo, "r") as entrada:
              leitor = csv.reader(entrada)

              for linha in leitor:
                  # Se a primeira linha for cabeçalho e não for o primeiro arquivo, pule
                  if i > 0 and "Mensagem" in linha[-1]:
                      continue
                  escritor.writerow(linha)
  
  for arquivo in csv_arquivos:
    try:
        os.remove(arquivo)
    except Exception as e:
        print(f"Erro ao apagar {arquivo}: {e}")

def copiar_csv(servers, clients, messages):

  soma = messages*clients
  if ((soma > 1000) or (soma/servers >= 500)):
    soma = soma//servers//150
    print(f"Aguardando {soma} segundos para garantir que todas as mensagens foram processadas...")
    time.sleep(soma)

  csv_arquivos = []

  pod_list = os.popen("kubectl get pod -l app=server -o name").read().strip().splitlines()

  for pod in pod_list:
    pod_name = pod.replace("pod/", "")
    dest = f"./csv/{pod_name}_{servers}_{clients}_{messages}.csv"
    ret = os.system(f"kubectl cp {pod_name}:log_clients.csv {dest}")
    if ret == 0 and os.path.exists(dest):
        csv_arquivos.append(dest)
        os.system(f"kubectl exec {pod_name} -- rm -f log_clients.csv")
    else:
        print(f"Arquivo log_clients.csv não encontrado no pod {pod_name}, ignorando.")

  unir_csv(csv_arquivos, servers, clients, messages)


for servers in server_counts:

    with open("server/deployment.yaml") as f:
        deployment = list(yaml.safe_load_all(f))

    for i, document in enumerate(deployment):
      if document and document.get('kind') == 'Deployment':
          # Modificar o número de réplicas
          document['spec']['replicas'] = servers
          print(f"Réplicas alteradas para: {servers}")
          break
      
    with open("temp-server-deployment.yaml", "w") as f:
        yaml.dump_all(deployment, f, sort_keys=False)

    # Atualiza o YAML do servidor
    os.system(f"kubectl delete deployment server --ignore-not-found")
    os.system(f"kubectl apply -f temp-server-deployment.yaml")
    os.system("kubectl rollout status deployment/server")
    os.system("kubectl wait --for=condition=ready pod -l app=server --timeout=60s")


    for clients in client_counts:
        for messages in message_counts:
            job_name = f"client-{servers}-{clients}-{messages}"

            print(f"Testando com {servers} servidores, {clients} clientes, {messages} mensagens")

            # Cria e aplica o job.yaml personalizado
            job_yaml = f"""
apiVersion: batch/v1
kind: Job
metadata:
  name: {job_name}
spec:
  parallelism: {clients}
  completions: {clients}
  template:
    spec:
      containers:
      - name: client
        image: tcp_client
        command: ["python", "client.py"]
        args: ["--host", "server", "--port", "50001", "--messages", "{messages}"]
        imagePullPolicy: Never
      restartPolicy: Never
  backoffLimit: 0
"""
            with open("temp-client-job.yaml", "w") as f:
                f.write(job_yaml)

            os.system("kubectl apply -f temp-client-job.yaml")
            os.system(f"kubectl wait --for=condition=complete job/{job_name} --timeout=120s")

            os.system(f"kubectl delete job {job_name} --ignore-not-found")
            os.system(f"kubectl wait --for=delete job/{job_name} --timeout=60s")

            # Copia CSV do servidor
            copiar_csv(servers, clients, messages)

    print("Fim do teste para", servers, "servidores\n")

# Limpeza dos arquivos temporários
print("Removendo arquivos temporários")
os.remove("temp-server-deployment.yaml")
os.remove("temp-client-job.yaml")

# Gera os gráficos
gerar_graficos()