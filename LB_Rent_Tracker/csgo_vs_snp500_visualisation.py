from heapq import merge
from numpy import datetime64
import pandas as pd
from datetime import datetime
from track_item_value import item_name_scmlink

today = datetime64(datetime.now())
merged_df = pd.DataFrame({'Date': pd.date_range('2021-01-01', today)})

skin_df = pd.read_csv('item_values_by_date/★ Bayonet | Black Laminate (Minimal Wear).csv', names=["Date", "Value", "TradingVolume"])
skin_df2 = pd.read_csv('item_values_by_date/★ Bayonet | Freehand (Field-Tested).csv', names=["Date", "Value", "TradingVolume"])

snp_df = pd.read_csv('tables/snp500_data.csv')
rent_df = pd.read_csv('tables/lootbear_revenue_data.csv')

snp_df['Date'] = pd.to_datetime(snp_df['Date'])
snp_df = snp_df[['Date', 'S&P_Gain', 'Investment_Gain']].set_index('Date')
snp_df = snp_df.rename(columns={"Investment_Gain": "S&P_Investing_Gain"})

rent_df['Date'] = pd.to_datetime(rent_df['Date'])
rent_df = rent_df.groupby(['Date']).mean()
rent_df = rent_df[['ROI', 'Cumulated_Revenue']]
rent_df = rent_df.rename(columns={"ROI": "ROI_Renting"})

def convert_df_to_wanted_format(df: pd.DataFrame, start, end):
    df['Date']=df['Date'].apply(lambda x: x[:-7])
    df['Date']=pd.to_datetime(df['Date'].apply(lambda x: datetime.strftime(datetime.strptime(x, '%b %d %Y'), '%Y-%m-%d')))
    df = df[df['Date'].between(start, end)]
    df.loc[df['Date'] == start, 'Invested'] = df.loc[df.index[df['Date'] == start], "Value"]

    return df

for item in item_name_scmlink.items():
    temp_df = pd.DataFrame({'Date': pd.date_range('2021-01-01', today)})
    df = pd.read_csv(f'item_values_by_date/{item[0]}.csv', names=["Date", "Value", "TradingVolume"])
    df = convert_df_to_wanted_format(df, item[1]['start'], item[1]['end'])
    temp_df = temp_df.join(df.set_index('Date'), on='Date')
    temp_df = temp_df.fillna(method='ffill')
    merged_df = pd.concat([merged_df, temp_df]).groupby(['Date']).sum().reset_index()


merged_df = merged_df.join(snp_df, on='Date')
merged_df = merged_df.join(rent_df, on='Date')
merged_df = merged_df.fillna(method='ffill')

moving_average_window = 10

merged_df['Value_rolling_avg'] = merged_df['Value'].rolling(window=moving_average_window, min_periods=1).mean()
merged_df['ROI_Skins'] = merged_df['Value_rolling_avg']/merged_df['Invested'].rolling(window=moving_average_window, min_periods=1).mean()
merged_df['ROI_Skins+Rent'] = (merged_df['Value_rolling_avg']+merged_df['Cumulated_Revenue'])/merged_df['Invested'].rolling(window=moving_average_window, min_periods=1).mean()

import plotly.express as px
import csv
import plotly.graph_objs as go

#fig = px.line(merged_df, x=merged_df['Date'], y=["S&P_Gain",  "ROI_Renting"])
#fig = px.line(merged_df, x=merged_df['Date'], y=["S&P_Gain", "ROI_Renting", "S&P_Investing_Gain", "ROI_Skins"])
fig = px.line(merged_df, x=merged_df['Date'], y=["S&P_Gain",  "ROI_Renting", "S&P_Investing_Gain", "ROI_Skins", "ROI_Skins+Rent"])

"""
with open('investments.csv', newline='') as f:
    reader = csv.reader(f)
    investments = list(reader)

investment_days = list(set(investment[0] for investment in investments))
for investment in investment_days:
    fig.add_vline(x=investment, line_width=1.5, line_dash="dash", line_color="green")
"""

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=30, label="1m", step="day", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

fig.show()
pd.set_option('display.max_rows', 50)
print(merged_df.head(n=267))
