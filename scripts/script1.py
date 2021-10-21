with open("./data/raw/CNAE_CBO_SEXO_2019.csv", "r") as f:
    file = (f.read())

file_list = file.splitlines()
del file_list[0]
file_list[0] = file_list[0].replace("; ;",";agregado;")
file_list[1] = ";" + file_list[1]

for line in file_list:
    if line == '':
        del file_list[file_list.index(line):]

new = "\n".join(file_list)

with open("./data/cleaned/CNAE_CBO_SEXO_2019.csv", "w") as w:
    w.write(new)
