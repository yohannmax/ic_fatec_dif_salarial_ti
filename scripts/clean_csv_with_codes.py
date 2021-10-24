import re

def clean_csv(csv_name):
    with open("./data/raw/" + csv_name, "r") as f:
        file = (f.read())

    file_list = file.splitlines()
    del file_list[0]
    del file_list[1]

    count = 0

    for line in file_list:
        if ":" in line:
            file_list[count] = line.replace(line[line.find(":"):line.find(";")],'')
        if line == '':
            del file_list[file_list.index(line):]
        count += 1

    new_csv = "\n".join(file_list)

    new_csv = re.sub(r'CBO 2002 Família', 'CBO', new_csv)
    new_csv = re.sub(r'620:Atividades dos serviços de tecnologia da informação',
                     r'620_M', new_csv, 1)
    new_csv = re.sub(r'620:Atividades dos serviços de tecnologia da informação',
                     r'620_F', new_csv, 1)
    new_csv = re.sub(r'631:Tratamento de dados. hospedagem na internet e outras atividades relacionadas',
                     r'631_M', new_csv, 1)
    new_csv = re.sub(r'631:Tratamento de dados. hospedagem na internet e outras atividades relacionadas',
                     r'631_F', new_csv, 1)
    new_csv = re.sub(r'\.','', new_csv)
    new_csv = re.sub(r',','.', new_csv)

    with open("./data/cleaned/" + csv_name, "w") as w:
        w.write(new_csv)

clean_csv("CNAE_CBO_SEXO_2019_freq.csv")