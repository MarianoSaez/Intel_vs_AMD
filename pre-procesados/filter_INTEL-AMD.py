import pandas as pd


# ============================== CSV para toda la muestra =====================
# df = pd.read_csv('pre-procesados/Cuentitas locas - Tabla cores-compresion.csv')

# for i in df.index:
#     if df.loc[i, 'Cpu name'] == 'No-Info' or\
#        df.loc[i, 'Cores'] == -1:
#         df.drop(i, inplace=True)

# df.to_csv('cores_compresion_all.csv', index=False, encoding='utf-8')

# ============================ CSV para AMD e Intel ===========================

df = pd.read_csv('pre-procesados/smallpt/smallpt_all.csv')

# AMD
# for i in df.index:
#     if 'AMD' not in df.loc[i, 'Cpu name']:
#         df.drop(i, inplace=True)

# df.to_csv('pre-procesados/smallpt/smallpt_amd.csv', index=False, encoding='utf-8')

# Intel
for i in df.index:
   if 'Intel' not in df.loc[i, 'Cpu name']:
       df.drop(i, inplace=True)

df.to_csv('pre-procesados/smallpt/smallpt_intel.csv', index=False, encoding='utf-8')
