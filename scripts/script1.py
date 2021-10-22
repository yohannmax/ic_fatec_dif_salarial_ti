import re

def clean_csv(csv_name):
    with open("./data/raw/" + csv_name, "r") as f:
        file = (f.read())

    file = re.sub(r'Média','mean', file)
    file = re.sub(r'Freq','freq', file)
    file = re.sub(r'Soma','sum', file)

    file_list = file.splitlines()
    del file_list[0]
    del file_list[1]
    file_list[0] = file_list[0].replace("; ;",";TIPO_DADO;")

    count = 0

    for line in file_list:
        if ":" in line and "sum" in line:
            file_list[count] = line.replace(line[line.find(":"):line.find(";")],'')
            cod = file_list[count][0:file_list[count].find(";")]
        if "freq" in line or "mean" in line:
            file_list[count] = cod + line 
        if line == '':
            del file_list[file_list.index(line):]
        count += 1

    new_csv = "\n".join(file_list)

    new_csv = re.sub(r'CBO 2002 Família', 'CBO_FAMIL', new_csv)
    new_csv = re.sub(r'620:Atividades dos serviços de tecnologia da informação',
                     r'620:M', new_csv, 1)
    new_csv = re.sub(r'620:Atividades dos serviços de tecnologia da informação',
                     r'620:F', new_csv, 1)
    new_csv = re.sub(r'631:Tratamento de dados. hospedagem na internet e outras atividades relacionadas',
                     r'631:M', new_csv, 1)
    new_csv = re.sub(r'631:Tratamento de dados. hospedagem na internet e outras atividades relacionadas',
                     r'631:F', new_csv, 1)
    new_csv = re.sub(r'\.','', new_csv)
    new_csv = re.sub(r',','.', new_csv)

    with open("./data/cleaned/" + csv_name, "w") as w:
        w.write(new_csv)