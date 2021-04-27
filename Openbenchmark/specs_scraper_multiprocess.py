from selenium import webdriver
import pandas as pd
import time
import multiprocessing as mp

# TODO: Implementar multihilos/multiprocesos

# ======================== INPUT =============================
link = 'https://openbenchmarking.org/test/pts/smallpt'          # Link to scrap
processno = 10                                                  # Processes No.


# Encontrar el valor numerico para un campo determinado
def find_num_in_text(substring, string: str):
    spec_list = string.splitlines()
    for i in range(len(spec_list)):
        if substring in spec_list[i]:
            aux = spec_list[i].split()
            for j in aux:
                try:
                    return int(j)
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


# Funcion target para procesos hijos
def scrap(rng: tuple):
    # Para la simplicidad del pasaje de parametros se hardcodea el link
    cpu_list = list()
    core_list = list()
    thread_list = list()

    driver = webdriver.Firefox()

    for i in range(rng[0], rng[1]):
        driver.get(link)
        time.sleep(2)
        try:
            cpu = driver.find_element_by_xpath(
                f'/html/body/div[1]/div/div[2]/div[7]/div[{i}]/div[1]/a')
        except:
            continue

        cpu.click()

        # Seguridad para que dar tiempo a cargar la pagina (uno nunca sabe)
        time.sleep(2)
        try:
            string = driver.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div[2]/div/pre[2]').text
        except:
            string = 'None'

        cpu = find_str_in_text('Model name', string)
        core = find_num_in_text('Core(s) per socket', string)
        thread = find_num_in_text('Thread(s) per core', string) * core

        cpu_list.append(cpu)
        core_list.append(core)
        thread_list.append(thread)

    partial_dataframe = pd.DataFrame({'Cpu name': cpu_list, 'Cores': core_list,
                                      'Threads': thread_list})

    for i in partial_dataframe.index:
        if partial_dataframe.loc[i, 'Cpu name'] == 'No-Info' or\
           partial_dataframe.loc[i, 'Cores'] == -1:
            partial_dataframe.drop(i, inplace=True)

    driver.close()

    return partial_dataframe


if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get(link)
    time.sleep(3)
    for i in range(1, 500):
        try:
            driver.find_element_by_xpath(
                f'/html/body/div[1]/div/div[2]/div[6]/div[{i}]')
        except:
            max_index = i
            break
    driver.close()

    print("=========  INFO  =========")
    print(f"Web target: {link}")
    print(f"No. of processes: {processno}")
    print(f"Max. index: {max_index}")
    print(f"CPUs per Child {max_index//processno}")

    param = list()
    for i in range(processno):
        param.append((i*max_index//processno, (i+1)*max_index//processno))

    with mp.Pool(processno) as p:
        result = p.map(scrap, param)

    df = pd.concat(result)

    try:
        df.to_csv('pre-procesados/cores_smallpt_all.csv',
                  index=False, encoding='utf-8')
    except FileNotFoundError:
        df.to_csv('cores_smallpt_all.csv',
                  index=False, encoding='utf-8')
