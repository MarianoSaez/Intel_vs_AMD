import pandas as pd

marcas = 'AMD INTEL'.split()
for marca in marcas:
    # Solo para intel
    if marca == 'INTEL':
        ex_gen_list = '-2:-3:-4:-5:-6'.split(':')
        word_list = 'Core i3:Core i5:Core i7:Core i9'.split(':')
    else:
        ex_gen_list = 'FX-:Epyc:Phenom:Athlon'.split(':')
        word_list = 'Ryzen 3:Ryzen 5:Ryzen 7:Ryzen 9:Ryzen Threadripper'.split(':')


    df_dicc = dict()

    for i in word_list:
        df_dicc[i] = list()

    for i in df_dicc:
        df = pd.read_csv(f'pre-procesados\cb-r23-multi_core\\benchmark-cb-r23-multi_core-{marca}.csv')
        for j in df.index:
            if i not in df.loc[j, 'CPU NAME']:
                df.drop(j, inplace=True)
        df_dicc[i] = df

    print(df_dicc)

    for i in df_dicc:
        for j in df_dicc[i].index:
            for k in ex_gen_list:
                if k in df_dicc[i].loc[j, 'CPU NAME']:
                    df_dicc[i].drop(j, inplace=True)
                    break

    # print(df_dicc)
    for i in df_dicc:
        df_dicc[i].to_csv(f'pre-procesados\cb-r23-multi_core\{i}.csv',
                        index=False,
                        encoding='utf-8')


