import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#------------------------função de consulta do índice no BCB----------------------#

def consulta_bcb(codigo_bcb):
    url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json'.format(codigo_bcb)
    df = pd.read_json(url)
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    return df

#------------------------atribuição dos índices em dataframes----------------------#

selic = pd.DataFrame()
ipca = pd.DataFrame()
igpm = pd.DataFrame()
cdi = pd.DataFrame()
tr = pd.DataFrame()
a = consulta_bcb(4390)#Selic
b = consulta_bcb(433)#IPCA
c = consulta_bcb(189)#IGP-M
d = consulta_bcb(4391)#CDI
e = consulta_bcb(7811)#TR
selic = a
ipca = b
igpm = c
cdi = d
tr = e

#----------------unir os dataframes para depois exportar------------------#
df = selic.merge(ipca, on='data')
df2 = df.merge(igpm, on='data')
df3 = df2.merge(cdi, on='data')
df_merged = df3.merge(tr, on='data')
df_merged.columns = ["Data", "Selic", "IPCA", "IGP-M", "CDI", "TR"]#ordena colunas

#--------------------------------exportar em pdf-----------------------------------#

fig, ax = plt.subplots(figsize = (12, 4))
ax.axis('tight')
ax.axis('off')
the_table = ax.table(cellText = df_merged.values, colLabels = df_merged.columns, loc = 'center')

pp = PdfPages("Dados Históricos-índices e taxas.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()
