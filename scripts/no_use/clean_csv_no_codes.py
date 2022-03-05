import re

def clean_csv(csv_name):
    with open("./data/raw/" + csv_name, "r") as f:
        file = (f.read())

    file_list = file.splitlines()
    del file_list[0]
    del file_list[1]

    count = 0

    for line in file_list:
        if line == '':
            del file_list[file_list.index(line):]
        count += 1

    new_csv = "\n".join(file_list)

    new_csv = re.sub(r'CBO 2002 Família', 'CBO', new_csv)
    new_csv = re.sub(r'Atividades dos serviços de tecnologia da informação',
                     r'620_M', new_csv, 1)
    new_csv = re.sub(r'Atividades dos serviços de tecnologia da informação',
                     r'620_F', new_csv, 1)
    new_csv = re.sub(r'Tratamento de dados. hospedagem na internet e outras atividades relacionadas',
                     r'631_M', new_csv, 1)
    new_csv = re.sub(r'Tratamento de dados. hospedagem na internet e outras atividades relacionadas',
                     r'631_F', new_csv, 1)
    new_csv = re.sub(r'DIRETORES DE SERVICOS DE INFORMATICA', '1236', new_csv)
    new_csv = re.sub(r'GERENTES DE TECNOLOGIA DA INFORMACAO', '1425', new_csv)
    new_csv = re.sub(r'ENGENHEIROS EM COMPUTACAO', '2122', new_csv)
    new_csv = re.sub(r'ESPECIALISTAS EM INFORMATICA', '2123', new_csv)
    new_csv = re.sub(r'ANALISTAS DE SISTEMAS COMPUTACIONAIS', '2124', new_csv)
    new_csv = re.sub(r'TECNICOS EM PROGRAMACAO', '3171', new_csv)
    new_csv = re.sub(r'TECNICOS EM OPERACAO E MONITORACAO DE COMPUTADORES', '3172', new_csv)
    new_csv = re.sub(r'\.','', new_csv)
    new_csv = re.sub(r',','.', new_csv)

    with open("./data/cleaned/" + csv_name, "w") as w:
        w.write(new_csv)

clean_csv("CNAE_CBO_SEXO_2019_sum.csv")