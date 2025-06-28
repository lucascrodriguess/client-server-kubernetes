import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def gerar_graficos():
    
    # Pasta onde os gráficos serão salvos
    output_dir = "./png"
    os.makedirs(output_dir, exist_ok=True)  # Cria a pasta se não existir

    for file in glob.glob("./csv/*"): # Pega todos os arquivos CSV na pasta ./csv
        df = pd.read_csv(file, header=None,
                        names=["timestamp", "ip", "port", "mensagem"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S.%f")

        # Contar mensagens por frações de segundo
        df.set_index("timestamp", inplace=True)
        df_resampled = df.resample("100ms").count()  # 100L = 100 ms

        # Nome legível para o gráfico
        nome_base = os.path.basename(file).replace(".csv", "").title()
        nome_arquivo = os.path.basename(file).replace(".csv", ".png")
        caminho_saida = os.path.join(output_dir, nome_arquivo)

        plt.figure(figsize=(10, 5))
        plt.plot(df_resampled.index, df_resampled["mensagem"])
        plt.title(f"{nome_base} - Mensagens por 100ms")
        plt.xlabel("Tempo")
        plt.ylabel("Número de mensagens")
        plt.grid()
        plt.tight_layout()
        plt.savefig(caminho_saida)  
        plt.close()

        print(f"Gráfico salvo em: {caminho_saida}")