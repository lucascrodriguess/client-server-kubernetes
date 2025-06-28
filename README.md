# Cliente-Servidor-Kubernetes

Este projeto implementa um sistema de testes de desempenho de comunicação TCP entre múltiplos clientes e servidores, utilizando Kubernetes para orquestração dos containers. O objetivo é analisar o comportamento do sistema sob diferentes cargas, coletar logs e gerar gráficos de desempenho.

## Estrutura do Projeto

- **server/**: Código-fonte e configuração do servidor TCP.
- **client/**: Código-fonte e configuração do cliente TCP.
- **automation.py**: Script principal para automação dos testes, coleta de logs e geração de gráficos.
- **graph.py**: Geração de gráficos a partir dos arquivos CSV.
- **requirements.txt**: Dependências Python do projeto.
- **csv/**: (Ignorado no Git) Armazena os arquivos de log gerados durante os testes.
- **png/**: (Ignorado no Git) Armazena os gráficos gerados.
- **venv/**: (Ignorado no Git) Ambiente virtual Python.
- **arquivos/**: (Ignorado no Git) Pasta para arquivos temporários ou auxiliares.

## Pré-requisitos

- Python 3.8+
- [Docker](https://www.docker.com/)
- [Kubernetes (kubectl)](https://kubernetes.io/docs/tasks/tools/)
- Ambiente com suporte a containers

## Instalação

1. Clone este repositório:
   ```sh
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd Cliente-Servidor-Kubernetes-2
   ```

2. Instale as dependências Python:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. Construa as imagens Docker:
   ```sh
   docker build -t tcp_server ./server
   docker build -t tcp_client ./client
   ```

## Execução dos Testes

1. Certifique-se de que o cluster Kubernetes está ativo.
2. Execute o script de automação:
   ```sh
   python automation.py
   ```
   O script irá:
   - Configurar e aplicar os deployments e jobs no Kubernetes.
   - Coletar os logs dos servidores.
   - Unificar os logs em arquivos CSV.
   - Gerar gráficos de desempenho na pasta `png/`.

## Resultados

- Os arquivos CSV com os logs ficam em `csv/`.
- Os gráficos gerados ficam em `png/`.

## Limpeza

O script `automation.py` remove arquivos temporários automaticamente ao final da execução.

## Observações

- As pastas `csv/`, `png/`, `venv/` e `arquivos/` estão no `.gitignore` e não são versionadas.
- Para alterar os parâmetros de teste (quantidade de servidores, clientes, mensagens), edite as listas no início do `automation.py`.

---

Desenvolvido para fins acadêmicos na disciplina de Redes de Computadores -