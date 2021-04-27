from selenium import webdriver
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
import os

# Variables que dependen de la pagina
XPATHINDEX = 6
LISTSZ_APX = 120
TEST = 'amg'

# TODO: Implementar multihilos/multiprocesos


# Encontrar el valor numerico para un campo determinado
def find_num_in_text(substring, string: str):
    spec_list = string.splitlines()
    for i in range(len(spec_list)):
        if substring in spec_list[i]:
            aux = spec_list[i].split()
            for j in aux:
                try:
                    return int(j.split('.')[0])
                except ValueError:
                    continue
    return -1


# Encontrar texto para un campo determinado
def find_str_in_text(subst, string: str):
    spec_list = string.splitlines()
    for i in range(len(spec_list)):
        if subst in spec_list[i]:
            aux = spec_list[i].split(":")
            for j in aux:
                try:
                    return aux[1].strip()
                except ValueError:
                    continue
    return "No-Info"


try:
    os.mkdir(f'pre-procesados/{TEST}')
except FileExistsError:
    print("No se creo el directorio porque ya existia")


link = f'https://openbenchmarking.org/test/pts/{TEST}'

cpu_list = list()
core_list = list()
thread_list = list()
percentile_list = list()
avg_list = list()
frec_list = list()

# Abrir el navegador y cargar pagina
driver = webdriver.Firefox()

# Bucle para obtener nucleos de un procesador (y mas info si queres)
for i in range(2, LISTSZ_APX):
    driver.get(link)
    time.sleep(1)

    try:
        aux = list()
        for j in range(2, 5):
            col = driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div[{XPATHINDEX}]/div[{i}]/div[{j}]')
            aux.append(col)

        percentile = aux[0].text
        avg = aux[2].text.split()[0]

    except NoSuchElementException:
        percentile = -1
        avg = -1


    try:
        cpu = driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div[{XPATHINDEX}]/div[{i}]/div[1]/a')
    except:
        print('====================\nTier-end')
        continue
    cpu.click()

    # Seguridad para que dar tiempo a cargar la pagina (uno nunca sabe)
    time.sleep(2)
    try:
        string = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/pre[2]').text
    except:
        string = 'None'

    cpu = find_str_in_text('Model name', string)
    core = find_num_in_text('Core(s) per socket', string)
    thread = find_num_in_text('Thread(s) per core', string) * core
    frec = find_num_in_text('CPU MHz', string)

    cpu_list.append(cpu)
    core_list.append(core)
    thread_list.append(thread)
    percentile_list.append(percentile)
    avg_list.append(avg)
    frec_list.append(frec)

df = pd.DataFrame({'Cpu name': cpu_list,
                   'Cores': core_list,
                   'Frec(MHZ)': frec_list,
                   'Threads': thread_list,
                   'Percentile': percentile_list,
                   'AVG': avg_list})

for i in df.index:
    if df.loc[i, 'Cpu name'] == 'No-Info' or\
       df.loc[i, 'Cores'] == -1:
        df.drop(i, inplace=True)

df.to_csv(f'pre-procesados/{TEST}/{TEST}_all.csv', index=False, encoding='utf-8')


driver.close()
