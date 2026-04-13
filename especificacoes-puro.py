import requests
import json
import csv


#Realizando a requisição dos arquivos através dos endpoints fornecidos
#pegar a informação do servidor e salvar como um arquivo json
def salvar_arquivo_api(nome_arquivo, url):
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(nome_arquivo, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Arquivo {nome_arquivo} salvo com sucesso!")
    else:
        print("Falha ao baixar o arquivo. Status:", response.status_code)

#le json
def ler_json(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def salvar_csv(nome_arquivo, dados):
    with open(nome_arquivo, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(dados) # Escreve várias linhas de uma vez




#main

salvar_arquivo_api("dados_propriedade.json", "https://granter-interview.s3.sa-east-1.amazonaws.com/dados_propriedade.json")
salvar_arquivo_api("propriedade.json","https://granter-interview.s3.sa-east-1.amazonaws.com/propriedades.json")
salvar_arquivo_api("risco_propriedade.json","https://granter-interview.s3.sa-east-1.amazonaws.com/risco_propriedade.json")


#ESPECIFICAÇÃO 1
#criar campo 'identificador' que seja a concatenação de "cd_oficial" com "nr_unidade_exploracao"

info_propriedade = ler_json('propriedade.json')

for item in info_propriedade["propriedade"]:
    item["identificador"] = str(item["cd_oficial"]) + str(item["nr_unidade_exploracao"])  # Adiciona o novo campo em cada objeto

with open('propriedade.json', 'w', encoding='utf-8') as f:
    json.dump(info_propriedade, f, indent=4, ensure_ascii=False)

print("especificação 1 OK")

#ESPECIFICAÇÃO 2

info_propriedade = ler_json('propriedade.json')["propriedade"]
info_dados_propriedade  = ler_json('dados_propriedade.json')["dados_propriedade"]

for propriedade in info_propriedade:
    for dado in info_dados_propriedade:
        if int(propriedade["identificador"]) == dado["cd_propriedade"]:
            propriedade["cd_especie"] = dado["cd_especie"]
            propriedade["qt_animais"] = dado["qt_animais"]
            break

with open('propriedade.json', 'w', encoding='utf-8') as f:
    json.dump(info_propriedade, f, indent=4, ensure_ascii=False)

print("especificação 2 OK")

#ESPECIFICAÇÃO 3

info_risco_propriedade = ler_json('risco_propriedade.json')["risco_propriedade"]


titulo_colunas = [
    ['Identificador', 'nm_propriedade', 'riscos','score_normalizado'],
]

linha=[]
riscos= ""
score = 0

salvar_csv('tabela_final.csv', titulo_colunas)

for item in info_propriedade:
    linha.append(item["identificador"])
    linha.append(item["nm_propriedade"])

    for dado in info_risco_propriedade:
        if int(item["id_propriedade"]) == dado["cd_propriedade"]:
            riscos = riscos + dado["nm_criterio"]
            if int(dado["score_criterio"])  != 0:
                riscos = riscos + "; "
            score += dado["score_criterio"] 
    
    linha.append(riscos)
    linha.append(score)
    riscos= ""
    score = 0
    salvar_csv('tabela_final.csv', [linha])
    linha.clear()


print("especificação 3 OK")


