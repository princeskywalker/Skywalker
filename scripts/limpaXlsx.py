import pandas as pd
from datetime import datetime
import re


arquivo_entrada = "data-filtered.xlsx"
arquivo_saida = input('Crie um nome para o arquivo: ')

df = pd.read_excel(arquivo_entrada, header=1, dtype=str)

df.columns = df.columns.str.strip().str.lower()

hoje = datetime.today()
def luhn_check(numero):
    numero = numero[::-1]
    soma = 0

    for i, digito in enumerate(numero):
        n = int(digito)

        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9

        soma += n

    return soma % 10 == 0

with open(arquivo_saida, "w", encoding="utf-8") as outfile:
    for _, row in df.iterrows():

        numero = str(row["cartao-numero"]).strip()
        mes = str(row["validade-mes"]).strip().zfill(2)
        ano = str(row["validade-ano"]).strip()
        cvv=str(row["cvv"]).strip().zfill(3)
        cpf=str(row["cpf"]).strip()

        # cria data de vencimento (último dia do mês)
        try:
            numero_limpo = re.sub(r"\D", "", numero)
            if not numero_limpo or not numero_limpo.isdigit():
                continue
            if not luhn_check(numero_limpo):
                continue

            if not luhn_check(numero):
                continue
            data_validade = datetime(int(ano), int(mes), 1)

            # considera vencido se ano/mês já passaram
            if data_validade < hoje.replace(day=1):
                continue  # pula cartão vencido

        except:
            continue  # pula se dados inválidos

        ultimos4 = numero
        validade_formatada = f"{mes}/{ano}"

        outfile.write(f"{ultimos4}|{validade_formatada}|{cvv}|{cpf}\n")

print("Arquivo gerado apenas com cartões válidos.")
