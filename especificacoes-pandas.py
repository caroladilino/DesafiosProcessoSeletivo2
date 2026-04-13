import requests
import json
import csv
import pandas as pd

#função que cria DataFrame
def carregar_df(url, chave):
    pedido = requests.get(url)
    data = pedido.json()
    return pd.DataFrame(data[chave])


#main

#chamando a função pra criar dfs para os 3 arquivos
df_propriedade = carregar_df("https://granter-interview.s3.sa-east-1.amazonaws.com/propriedades.json", "propriedade")
df_dados_propriedade = carregar_df("https://granter-interview.s3.sa-east-1.amazonaws.com/dados_propriedade.json", "dados_propriedade")
df_risco_propriedade = carregar_df("https://granter-interview.s3.sa-east-1.amazonaws.com/risco_propriedade.json", "risco_propriedade")


### ESPECIFICAÇÃO 1 ###

#ao invés de baixar o arquivo e escrever nele, só itera linha por linha (e index) pra criar a coluna identificador c valor correto
for index, linha in df_propriedade.iterrows():
    identificador = str(linha['cd_oficial']) + str(linha['nr_unidade_exploracao']) #concatenação
    df_propriedade.at[index, 'identificador'] = identificador

print("especificação 1 OK")


### ESPECIFICAÇÃO 2 ###

df_propriedade['cd_especie'] = None
df_propriedade['qt_animais'] = None

#esse foi exatamente o mesmo código de antes, só mudando os comandos pra usar o pandas
for i, propriedade in df_propriedade.iterrows():
    for j, dado in df_dados_propriedade.iterrows():
        if int(propriedade["identificador"]) == int(dado["cd_propriedade"]):
            df_propriedade.at[i, "cd_especie"] = df_dados_propriedade.at[j, "cd_especie"]
            df_propriedade.at[i, "qt_animais"] = df_dados_propriedade.at[j, "qt_animais"]
            break

print("especificação 2 OK")


### ESPECIFICAÇÃO 3 ###

lista=[]

#lógica parecida com antes, só mudou que agr adiciona todas as linhas na lista como um dicionário e manda pro csv uma vez só 
for i, propriedade in df_propriedade.iterrows():
    riscos = []
    score = 0
    for j, risco in df_risco_propriedade.iterrows():
        if int(risco["cd_propriedade"]) == int(propriedade["id_propriedade"]):
            riscos.append(str(risco['nm_criterio']))
            score += risco['score_criterio']

    lista.append({
        'identificador': propriedade['identificador'],
        'nm_propriedade': propriedade['nm_propriedade'],
        'riscos': "; ".join(riscos),
        'score_normalizado': score
    })

df_final = pd.DataFrame(lista)
df_final.to_csv('tabela_final.csv', index=False, encoding='utf-8-sig')
