from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

link_list = ['cpu_benchmark-cinebench_r23_single_core-15',
             'cpu_benchmark-cinebench_r23_multi_core-16',
             'cpu_benchmark-cinebench_r20_single_core-9',
             'cpu_benchmark-cinebench_r20_multi_core-10',
             'cpu_benchmark-geekbench_5_single_core-13',
             'cpu_benchmark-geekbench_5_multi_core-14',
             'cpu_benchmark-blender_2_81_bmw27-12']

for i in link_list:
    cpu_list = list()
    benchmark_list = list()

    driver = webdriver.Firefox()
    driver.get(f'https://www.cpu-monkey.com/es/{i}')
    driver.find_element_by_xpath('//*[@id="load_benchmarks"]').click()

    # No es lo mas eficiente pero hace el trabajo
    time.sleep(5)

    # Entrar a cada CPU y recolectar datos del mismo
    

    content = driver.page_source
    soup = BeautifulSoup(content)
    for cpu in soup.findAll('a', href=True, attrs={'class': 'black'}):
        cpu_list.append(cpu.text)

    for benchmark in soup.findAll('div', attrs={'class': 'benchmarkbar'}):
        benchmark_list.append(benchmark.text)

    df = pd.DataFrame({'Cpu name': cpu_list, 'Score': benchmark_list})
    df.to_csv(f'MonkeyCPU-{i}.csv', index=False, encoding='utf-8')

    driver.close()
