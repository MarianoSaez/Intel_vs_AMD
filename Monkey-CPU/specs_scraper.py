# Specs Scraper para la pagina de https://www.cpu-monkey.com
from selenium import webdriver
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException

LINK_LIST = ['cpu_benchmark-cinebench_r23_single_core-15',
             'cpu_benchmark-cinebench_r23_multi_core-16',
             'cpu_benchmark-cinebench_r20_single_core-9',
             'cpu_benchmark-cinebench_r20_multi_core-10',
             'cpu_benchmark-geekbench_5_single_core-13',
             'cpu_benchmark-geekbench_5_multi_core-14',
             'cpu_benchmark-blender_2_81_bmw27-12']
FREC_XPATH = '/html/body/div[4]/div[5]/div[3]/table[1]/tbody/tr[2]/td[2]'
CORES_XPATH = '/html/body/div[4]/div[5]/div[3]/table[1]/tbody/tr[2]/td[4]'
CPU_ENTRY_XPATH = '/html/body/div[4]/div[5]/div[2]/table/tbody'


def webElement_to_text(webElement_array: list):
    text_list = list()
    for i in webElement_array:
        text_list.append(i.text)
    return text_list


for i in LINK_LIST:
    cpu_list = list()
    benchmark_list = list()
    frec_list = list()
    core_list = list()

    driver = webdriver.Firefox()
    driver.get(f'https://www.cpu-monkey.com/en/{i}')
    driver.find_element_by_xpath('//*[@id="load_benchmarks"]').click()

    time.sleep(5)

    try:
        # Obtener nombre y puntaje la la CPU
        webElement_cpu_list = driver.find_elements_by_class_name('black')
        cpu_list = webElement_to_text(webElement_cpu_list)
        benchmark_list = webElement_to_text(driver.find_elements_by_class_name('benchmarkbar'))

        cpu_link_list = list()
        for j in webElement_cpu_list:
            cpu_link_list.append(j.get_attribute('href'))

        for j in cpu_link_list:
            driver.get(f'{j}')
            aux = driver.find_elements_by_class_name('dtcpu')
            for k in range(len(aux)):
                print(aux[k].text)
                if 'Frequency:' in aux[k].text:
                    frec_list.append(aux[k+1].text)
                    continue
                if 'CPU Cores:' in aux[k].text:
                    core_list.append(aux[k+1].text)
                    continue

    except NoSuchElementException as e:
        print(f'Error {e}')
        df = pd.DataFrame({'Cpu name': cpu_list, 'Score': benchmark_list})
        df.to_csv(f'MonkeyCPU-{i}.csv', index=False, encoding='utf-8')
        break

    df = pd.DataFrame({'CPU NAME': cpu_list, 'BENCHMARK': benchmark_list,
                       'FREC': frec_list, 'CORES': core_list})
    df.to_csv(f'Monkey-CPU/MonkeyCPU-{i}.csv', index=False, encoding='utf-8')

    driver.close()
