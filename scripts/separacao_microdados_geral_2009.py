import pandas as pd
import glob

ano = '2009'

list_files = glob.glob("C:/Users/YOHANNGABRIELOLIANIF/" + ano + "/*/*.txt")

cbo_familia = ('1236','1425','2122','2124','3171','3172','2123')

col_list = ['Bairros SP', 'Bairros Fortaleza', 'Bairros RJ', 'Causa Afastamento 1', 'Causa Afastamento 2', 'Causa Afastamento 3', 
            'Motivo Desligamento', 'CNAE 95 Classe', 'Distritos SP', 'Faixa Etária', 'Faixa Hora Contrat', 'Faixa Remun Dezem (SM)', 
            'Faixa Remun Média (SM)', 'Faixa Tempo Emprego', 'Qtd Hora Contr', 'Ind CEI Vinculado', 'Ind Simples', 'Mês Admissão', 
            'Mês Desligamento', 'Mun Trab', 'Município', 'Nacionalidade', 'Natureza Jurídica', 'Ind Portador Defic', 'Qtd Dias Afastamento', 
            'Regiões Adm DF', 'Vl Remun Dezembro (SM)', 'Vl Remun Média Nom', 'Vl Remun Média (SM)', 'CNAE 2.0 Subclasse', 
            'Tamanho Estabelecimento', 'Tempo Emprego', 'Tipo Admissão', 'Tipo Estab', 'Tipo Estab.1', 'Tipo Defic', 'Tipo Vínculo']

for file in list_files:
    # Leitura do CSV do estado atual:
    df = pd.read_csv(file, sep = ";", encoding = 'latin-1', dtype = object)

    # Elimina as colunas na col_list:
    df.drop(col_list, inplace = True, axis = 1)

    # Filtra para somente com vínculo ativo 31/12:
    df = df[df["Vínculo Ativo 31/12"] == '1']

    # Retira a coluna do vínculo, que não é mais necessária:
    df.drop("Vínculo Ativo 31/12", inplace = True, axis = 1)
    
    # Retira salários zerados:
    df = df[df["Vl Remun Dezembro Nom"] != '0000000000,00']

    # Transforma as remunerações em flutuante:
    df['Vl Remun Dezembro Nom'] = df['Vl Remun Dezembro Nom'].str.lstrip('0')       # Tira zero a esquerda
    df['Vl Remun Dezembro Nom'] = df['Vl Remun Dezembro Nom'].str.replace(',','.')  # Substitui a virgula por ponto

    # Filtra as famílias que deve pegar:
    df = df[df["CBO Ocupação 2002"].str.startswith(cbo_familia)]

    # Cria a coluna UF e insere o estado atual:
    df.insert(0, "UF", file[-10:-8])

    print(len(df))

    # Salva em um novo csv para o estado atual:
    df.to_csv("C:/Users/YOHANNGABRIELOLIANIF/" + ano + "/dados/" + file[-10:-4] + ".csv", index = False, sep = ';', encoding = 'utf-8')

# Realiza a leitura de cada arquivo CSV e junta em um somente:

list_files = glob.glob("C:/Users/YOHANNGABRIELOLIANIF/" + ano + "/dados/*.csv")

df_final = pd.read_csv(list_files[0], sep = ";", encoding = 'utf-8', dtype = object)
list_files
del list_files[0]

for file in list_files:
    df = pd.read_csv(file, sep = ";", encoding = 'utf-8', dtype = object)
    
    df_final = pd.concat([df_final, df], ignore_index = True, sort = False)


df_final.to_csv("./data/raw/DATA_RAIS_" + ano + ".csv", index = False, sep = ";", encoding='utf-8')