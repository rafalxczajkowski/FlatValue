import pandas as pd
import plotly.express as px

df_his = pd.read_csv('data/historia-kredytu-2008.csv', encoding='Windows-1250')
df_chf = pd.read_csv('data/CHF.csv', encoding='Windows-1250',
                     sep=';', parse_dates=['Data'])

df_his['#Data księgowania'] = pd.to_datetime(
    df_his['#Data księgowania'], format="%d-%m-%Y")
df_his_short = df_his.loc[df_his['#Opis'].str.contains(
    'SPŁATA'), ['#Data księgowania', '#Kwota', '#Kwota pozostała do spłaty']]
df_his_short.columns = ['Date', 'CHF amount', 'CHF left to pay']

df_chf_short = df_chf.loc[:, ['Data', 'CHF (Cena sprzedazy)']]
df_chf_short.columns = ['Date', 'CHF rate']

# Remove time part from Timestamp
df_chf_short.loc[:, 'Date'] = df_chf_short['Date'].dt.normalize()
# Merge history of payments df and CHF rates df
df_his_chf = pd.merge_asof(df_his_short, df_chf_short, on='Date')
# Add columns with calculated amounts to PLN and cumulative sum
df_his_chf.loc[:, "PLN amount"] = df_his_chf['CHF amount'] * df_his_chf['CHF rate']
df_his_chf.loc[:, "PLN left to pay"] = df_his_chf['CHF left to pay'] * df_his_chf['CHF rate']
df_his_chf.loc[:, "Sum of payments in PLN"] = df_his_chf['PLN amount'].cumsum()
# Change 0's to None
df_his_chf.loc[df_his_chf['CHF left to pay'] == 0, ['CHF left to pay']] = None
df_his_chf.loc[df_his_chf['PLN left to pay'] == 0, ['PLN left to pay']] = None
# df without None for plotting
df_his_chf_na = df_his_chf.dropna(how="any")
# create plot
fig = px.line(df_his_chf_na, x="Date", y=['Sum of payments in PLN', 'PLN left to pay'],
              title='Paying off CHF mortgage',
              width=1000,
              height=600)
# create html code containing the plot
def create_html():
    return fig.to_html("index.html", include_plotlyjs='cdn', full_html=True)
