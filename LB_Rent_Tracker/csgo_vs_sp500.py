from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import csv
import numpy as np

import plotly.graph_objs as go

snp_data = pd.DataFrame(yf.download("^GSPC", period="380d", interval="1d"))

with open('investments.csv', newline='') as f:
    reader = csv.reader(f)
    investments = list(reader)


def next_day(date:str) -> str:
    """returns the next date"""
    return str(datetime.strptime(date, "%Y-%m-%d").date() + timedelta(days=1))
def prev_day(date:str) -> str:
    """returns the previous date"""
    return str(datetime.strptime(date, "%Y-%m-%d").date() - timedelta(days=1))
def get_previous_trade_day(date: str) -> str:
    """returns the previous day when the stock market was open to trade"""
    prevdate = prev_day(date)
    try:
        snp_data.loc[prevdate]
        return prevdate
    except:
        return get_previous_trade_day(prevdate)
def get_next_trade_day(date: str) -> str:
    """returns the next day when the stock market was open to trade"""
    try:
        snp_data.loc[date]
        return date
    except:
        return get_previous_trade_day(next_day(date))

snp_data["S&P_Gain"] = snp_data["Close"]/snp_data.loc[get_next_trade_day(investments[0][0]),"Open"]
snp_data["Invested_today"] = 0
snp_data["Invested"] = 0
snp_data["Investment_Value"] = 0
snp_data["Investment_Gain"] = 0
# Alle Tage des S&P500 Kurses vor dem ersten Kauf werden ausgeblendet
snp_data.loc[snp_data.index <= get_next_trade_day(investments[0][0]), 'S&P_Gain'] = np.NaN


def add_investment(date:str, amount:float) -> None:
    """Es wird das Investment im Dataframe vermerkt. Ist an dem Tag, an dem ein Skin gekauft wurde
    die Börse geschlossen, so wird der Eintrag am daraufkommenden Börsentag eingetragen"""
    try:
        snp_data.loc[date, "Invested_today"] += int(amount)
    except:
        nextday = next_day(date)
        add_investment(nextday, amount)
        pass

# Filling the dataframe with the invested amounts 
for invest in investments:
    # invest ist [date, amount]
    add_investment(invest[0], invest[1])

snp_data["Invested"] = snp_data["Invested_today"].cumsum()


# ADDING INVESTMENT VALUE DATA
for i, index in enumerate(snp_data.index):
    index = str(index.date())

    todays_gain = snp_data.loc[index, "Close"]/snp_data.loc[index, "Open"]

    # Für den ersten Tag gibt es keinen vorherigen Handelstag
    # Daher würde hier eine unendliche Rekursion in der get_previous_trade_day Funktion entstehen
    if i != 0:
        previous_trade_day = get_previous_trade_day(index)
        gain_since_prev_day_close = snp_data.loc[index, "Close"]/snp_data.loc[previous_trade_day, "Close"]
        snp_data.loc[index, "Investment_Value"]  = snp_data.loc[previous_trade_day, "Investment_Value"] * gain_since_prev_day_close + snp_data.loc[index, "Invested_today"] * todays_gain
    else:
        snp_data.loc[index, "Investment_Value"] = snp_data.loc[index, "Invested_today"] * todays_gain

#INVESTMENT GAIN DATA
snp_data["Investment_Gain"] = snp_data["Investment_Value"]/snp_data["Invested"]

"""
fig = go.Figure()

fig.add_trace(go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'], name = 'market data'))

# Add titles
fig.update_layout(
    title='Uber live share price evolution',
    yaxis_title='Stock Price (USD per Shares)')

# X-Axes
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=30, label="1d", step="day", stepmode="backward"),
            dict(count=19, label="1m", step="month", stepmode="backward"),
            dict(step="all")
        ])
    )
)

#Show
fig.show()
"""


# PLOTTING CSGO SKINS

def change_date_format(date:str) -> str:
    
    date = date.split(' ')[0]
    date = datetime.strptime(date, '%d/%m/%Y')
    return datetime.strftime(date, '%Y-%m-%d')

df = pd.read_csv('rent_revenue_data.csv')

# 13321807 - ID des ersten relevaten Vermietungstermin
df = df[df["ID"] >= 13321807]

df["Date"] = df["Date"].map(change_date_format)

df = df[::-1]

df["Cumulated_Revenue"] = df["Revenue"].cumsum()
df["Invested"] = 0

def add_investment(date:str, amount:float) -> None:
    """Es wird das Investment im Dataframe vermerkt. Ist an dem Tag, an dem ein Skin gekauft wurde
    die Börse geschlossen, so wird der Eintrag am daraufkommenden Börsentag eingetragen"""
    try:
        df.loc[min(df.index[df["Date"] == date]), "Invested"] += int(amount)
    except:
        nextday = next_day(date)
        add_investment(nextday, amount)
        pass

for invest in investments:
    # invest ist [date, amount]
    add_investment(invest[0], invest[1])
    pass


df["Invested"] = df["Invested"].cumsum()
df["ROI"] = df["Cumulated_Revenue"]/df["Invested"]+1


import plotly.express as px

fig = px.line(snp_data, x=snp_data.index, y=["Investment_Gain", "S&P_Gain"])

investment_days = list(set(investment[0] for investment in investments))
for investment in investment_days:
    fig.add_vline(x=investment, line_width=1.5, line_dash="dash", line_color="green")
#sfig.add_hrect(y0=0.85, y1=1, line_width=0, fillcolor="red", opacity=0.2)

fig.add_trace(go.Scatter(x=df["Date"], y=df["ROI"], name = "Skin Renting ROI - excluding Skin Value"))


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

df.to_csv('tables/lootbear_revenue_data.csv')
snp_data.to_csv('tables/snp500_data.csv')