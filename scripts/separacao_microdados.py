import pandas as pd
import glob

list_files = glob.glob("C:/Users/YOHANNGABRIELOLIANIF/2009/*/*.csv")

for file in list_files:
    df = pd.read_csv(file, sep = ";", encoding = 'latin-1', dtype = object)
    print(list(df.columns))

cbo_familia = ('1236','1425','2122','2124','3171','3172','2123')
cnae_grupo = ('620','631')

col_list = ['Bairros SP', 'Bairros Fortaleza', 'Bairros RJ', 'Causa Afastamento 1', 'Causa Afastamento 2', 'Causa Afastamento 3', 
            'Motivo Desligamento', 'CNAE 95 Classe', 'Distritos SP', 'Faixa Etária', 'Faixa Hora Contrat', 'Faixa Remun Dezem (SM)', 
            'Faixa Remun Média (SM)', 'Faixa Tempo Emprego', 'Qtd Hora Contr', 'Ind CEI Vinculado', 'Ind Simples', 'Mês Admissão', 
            'Mês Desligamento', 'Mun Trab', 'Município', 'Nacionalidade', 'Natureza Jurídica', 'Ind Portador Defic', 'Qtd Dias Afastamento', 
            'Regiões Adm DF', 'Vl Remun Dezembro (SM)', 'Vl Remun Média Nom', 'Vl Remun Média (SM)', 'CNAE 2.0 Subclasse', 
            'Tamanho Estabelecimento', 'Tempo Emprego', 'Tipo Admissão', 'Tipo Estab', 'Tipo Estab.1', 'Tipo Defic', 'Tipo Vínculo']

for file in list_files:
    df = pd.read_csv(file, sep = ";", encoding = 'latin-1', dtype = object, index_col = 0)

    df.drop(col_list, inplace = True, axis = 1)
    df = df[df["Vínculo Ativo 31/12"] == '1']
    df = df[df["CBO Ocupação 2002"].str.startswith(cbo_familia)]
    df = df[df["CNAE 2.0 Classe"].str.startswith(cnae_grupo)]

    print(len(df))

    df.to_csv("C:/Users/YOHANNGABRIELOLIANIF/2009/dados/" + file[-10:-4] + ".csv")