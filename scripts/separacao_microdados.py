'''
Script para leitura, limpeza e junção dos dados retirados da base de microdados do
ministério da economia, RAIS.

Para o ano de 2009 são dados separados por estados em arquivo txt.
Para o ano de 2019 são dados separados por regiões em arquivo txt.

Cada um dos anos tem um conjunto diferentes de colunas a serem removidas, o restante é muito semelhante.

Também existe a possibilidade de isolar os setores de TI ou somente por CBO.
'''

import time
import pandas as pd
import glob

cbo_familia = ('1236','1425','2122','2124','3171','3172','2123')
cnae_grupo = ('620','631')

print("###################################\n")
print("Separação de dados RAIS\n")

sum_dados = 0
processar = False

while processar == False:
    ano = str(input("Escolha o ano: 2009 ou 2019: "))
    filtro_setor = input("Realizar filtro por setores de TI (S)/(N): ")

    if ano == '2009':
        processar = True
        colunas_remover = ['Bairros SP', 'Bairros Fortaleza', 'Bairros RJ', 'Causa Afastamento 1', 'Causa Afastamento 2', 'Causa Afastamento 3', 
                'Motivo Desligamento', 'CNAE 95 Classe', 'Distritos SP', 'Faixa Etária', 'Faixa Hora Contrat', 'Faixa Remun Dezem (SM)', 
                'Faixa Remun Média (SM)', 'Faixa Tempo Emprego', 'Qtd Hora Contr', 'Ind CEI Vinculado', 'Ind Simples', 'Mês Admissão', 
                'Mês Desligamento', 'Mun Trab', 'Município', 'Nacionalidade', 'Natureza Jurídica', 'Ind Portador Defic', 'Qtd Dias Afastamento', 
                'Regiões Adm DF', 'Vl Remun Dezembro (SM)', 'Vl Remun Média Nom', 'Vl Remun Média (SM)', 'CNAE 2.0 Subclasse', 
                'Tamanho Estabelecimento', 'Tempo Emprego', 'Tipo Admissão', 'Tipo Estab', 'Tipo Estab.1', 'Tipo Defic', 'Tipo Vínculo']
    elif ano == '2019':
        processar = True
        colunas_remover = ['Bairros SP', 'Bairros Fortaleza', 'Bairros RJ', 'Causa Afastamento 1', 'Causa Afastamento 2', 'Causa Afastamento 3', 
                'Motivo Desligamento', 'CNAE 95 Classe', 'Distritos SP', 'Faixa Etária', 'Faixa Hora Contrat', 'Faixa Remun Dezem (SM)', 
                'Faixa Remun Média (SM)', 'Faixa Tempo Emprego', 'Qtd Hora Contr', 'Ind CEI Vinculado', 'Ind Simples', 'Mês Admissão', 
                'Mês Desligamento', 'Mun Trab', 'Nacionalidade', 'Natureza Jurídica', 'Ind Portador Defic', 'Qtd Dias Afastamento', 
                'Regiões Adm DF', 'Vl Remun Dezembro (SM)', 'Vl Remun Média Nom', 'Vl Remun Média (SM)', 'CNAE 2.0 Subclasse', 
                'Tamanho Estabelecimento', 'Tempo Emprego', 'Tipo Admissão', 'Tipo Estab', 'Tipo Estab.1', 'Tipo Defic', 'Tipo Vínculo', 
                'IBGE Subsetor', 'Vl Rem Janeiro CC', 'Vl Rem Fevereiro CC', 'Vl Rem Março CC', 'Vl Rem Abril CC', 'Vl Rem Maio CC', 
                'Vl Rem Junho CC', 'Vl Rem Julho CC', 'Vl Rem Agosto CC', 'Vl Rem Setembro CC', 'Vl Rem Outubro CC',
                'Vl Rem Novembro CC', 'Ano Chegada Brasil', 'Ind Trab Intermitente', 'Ind Trab Parcial']

        uf = {'11':'RO','12':'AC','13':'AM','14':'RR','15':'PA','16':'AP','17':'TO','21':'MA',
                '22':'PI','23':'CE','24':'RN','25':'PB','26':'PE','27':'AL','28':'SE','29':'BA',
                '31':'MG','32':'ES','33':'RJ','35':'SP','41':'PR','42':'SC','43':'RS','50':'MS',
                '51':'MT','52':'GO','53':'DF'}
    else:
        print("Ano inválido!")

print("\nProcessando...")

tempo_inicial = time.time()

if ano == '2009':
    list_files = glob.glob("C:/Users/YOHANNGABRIELOLIANIF/Documents/OneDrive/ARQUIVOS_GERAIS/FATEC_ADS/IC/DADOS_BRUTOS/" + ano + "/*/*.txt")
else:
    list_files = glob.glob("C:/Users/YOHANNGABRIELOLIANIF/Documents/OneDrive/ARQUIVOS_GERAIS/FATEC_ADS/IC/DADOS_BRUTOS/" + ano + "/*.txt")

for file in list_files:
    # Leitura do CSV do estado ou região atual:
    df = pd.read_csv(file, sep = ";", encoding = 'latin-1', dtype = object)

    # Elimina as colunas na lista colunas_remover:
    df.drop(colunas_remover, inplace = True, axis = 1)

    # Filtra somente com vínculo ativo 31/12:
    df = df[df["Vínculo Ativo 31/12"] == '1']

    # Retira a coluna anterior do vínculo, que não é mais necessária:
    df.drop("Vínculo Ativo 31/12", inplace = True, axis = 1)
    
    # Retira salários zerados:
    df = df[df["Vl Remun Dezembro Nom"] != '0000000000,00']

    # Transforma as remunerações em flutuante:
    df['Vl Remun Dezembro Nom'] = df['Vl Remun Dezembro Nom'].str.lstrip('0')       # Tira zero a esquerda
    df['Vl Remun Dezembro Nom'] = df['Vl Remun Dezembro Nom'].str.replace(',','.')  # Substitui a virgula por ponto

    # Realiza o filtro pelas famílias de CBOs:
    df = df[df["CBO Ocupação 2002"].str.startswith(cbo_familia)]

    # Realiza o filtro dos setores de TI, caso escolhido a opção:
    if filtro_setor == 'S':
        df = df[df["CNAE 2.0 Classe"].str.startswith(cnae_grupo)]

    # Cria a coluna UF e insere o estado atual:
    if ano == '2019': # para dados de 2009
        df.insert(0, "UF", df["Município"].str[0:2])
        df["UF"].replace(uf, inplace = True)
        df.drop("Município", inplace = True, axis = 1)
    else: # para dados de 2019:
        df.insert(0, "UF", file[-10:-8])

    # Exibe o total de dados separados para o arquivo atual:
    sum_dados += len(df)
    print("\nTotal de casos separados: " + str(len(df)) + "\npara o arquivo: " + file)

    # Salva em um novo csv para o estado atual:
    if ano == '2009':
        df.to_csv("C:/Users/YOHANNGABRIELOLIANIF/Documents/OneDrive/ARQUIVOS_GERAIS/FATEC_ADS/IC/DADOS_BRUTOS/" + ano + "/dados/" + file[-10:-4] + ".csv", index = False, sep = ';', encoding = 'utf-8')
    else:
        df.to_csv("C:/Users/YOHANNGABRIELOLIANIF/Documents/OneDrive/ARQUIVOS_GERAIS/FATEC_ADS/IC/DADOS_BRUTOS/" + ano + "/dados/" + file[file.find("PUB_")+4:-4] + ".csv", index = False, sep = ';', encoding = 'utf-8')


# Realiza a leitura de cada arquivo CSV e junta em um somente:

print("\nSalvando o arquivo final...\n")

list_files = glob.glob("C:/Users/YOHANNGABRIELOLIANIF/Documents/OneDrive/ARQUIVOS_GERAIS/FATEC_ADS/IC/DADOS_BRUTOS/" + ano + "/dados/*.csv")

df_final = pd.read_csv(list_files[0], sep = ";", encoding = 'utf-8', dtype = object)
list_files
del list_files[0]

for file in list_files:
    df = pd.read_csv(file, sep = ";", encoding = 'utf-8', dtype = object)
    
    df_final = pd.concat([df_final, df], ignore_index = True, sort = False)

if filtro_setor == 'S':
    df_final.to_csv("./data/raw/DATA_RAIS_SETORTI_" + ano + ".csv", index = False, sep = ";", encoding='utf-8')
else:
    df_final.to_csv("./data/raw/DATA_RAIS_GERAL_" + ano + ".csv", index = False, sep = ";", encoding='utf-8')

tempo_final= time.time()
print("\nTotal de itens: " + str(sum_dados))
print("\n{:.1f} segundos".format(tempo_final - tempo_inicial))

print("\n###################################")