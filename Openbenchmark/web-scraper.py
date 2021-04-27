from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

link_list = ['compress-7zip', 'compress-gzip', 'compress-pbzip2', 'aobench', 'smallpt', 'ttsiod-renderer', 'openvkl']

for j in link_list:
    data = list()
    raw_data = list()
    row_list = list()


    driver = webdriver.Firefox()
    driver.get(f'https://openbenchmarking.org/test/pts/{j}')
    driver.find_element_by_xpath('//*[@id="results"]').click()

    # No es lo mas eficiente pero hace el trabajo
    time.sleep(5)

    content = driver.page_source
    soup = BeautifulSoup(content)
    for cpu in soup.findAll(attrs={'class': 'div_table_cell'}):
        data.append(cpu.text)
    
    
    for i in data:
        if len(row_list) < 4:
            row_list.append(i)
        if len(row_list) == 4:
            raw_data.append(row_list)
            row_list = list()
    cpu_list = list()
    percentile_list = list()
    avg_list = list()
    std_list = list()

    del raw_data[0]

    a = [x for x in range(len(raw_data)) if raw_data[x][0]=='Mid-Tier']
    del raw_data[a[0]]
    b = [x for x in range(len(raw_data)) if raw_data[x][0]=='Median']
    del raw_data[b[0]]
    c = [x for x in range(len(raw_data)) if raw_data[x][0]=='Low-Tier']
    del raw_data[c[0]]
    d = [x for x in range(len(raw_data)) if raw_data[x][0]=='Instruction Set']
    if d != []:
        del raw_data[d[0]]
    e = [x for x in range(len(raw_data)) if raw_data[x][0]=='Used by default on supported hardware.\xa0']
    if e != []:
        del raw_data[e[0]]
    f = [x for x in range(len(raw_data)) if raw_data[x][0]=='VEXTRACTF128 VZEROUPPER VINSERTF128']
    if f != []:
        del raw_data[f[0]]
    g = [x for x in range(len(raw_data)) if raw_data[x][0]=='VINSERTF128 VZEROUPPER']
    if g != []:
        del raw_data[g[0]]



    for i in raw_data:
        cpu_list.append(i[0])
        percentile_list.append(i[1])
        x = i[3].split()
        if len(x) == 3:
            avg_list.append(x[0])
            std_list.append(x[2])
        if len(x) == 1:
            avg_list.append(i[3])
            std_list.append('-')
    
    print(cpu_list)
    print(len(percentile_list))
    print(len(avg_list))
    print(len(std_list))
        

        
    df = pd.DataFrame({'Cpu name': cpu_list, 'Percentile': percentile_list, 'Average': avg_list, 'St D': std_list })
    df.to_csv(f'OpenBenchmarking-{j}.csv', index=False, encoding='utf-8')

    driver.close()