import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

"""TESLA"""
tesla = yf.Ticker("TSLA")

tesla_data = tesla.history(period='max')

tesla_data.reset_index(inplace=True)
# print(tesla_data.head())

tesla_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'

html_data = requests.get(tesla_url).text
soup = BeautifulSoup(html_data, 'html5lib')

read_html_tesla_data = pd.read_html(tesla_url)
tesla_revenue = read_html_tesla_data[1]

# print(tesla_revenue.columns)
tesla_revenue.rename(columns={'Tesla Quarterly Revenue (Millions of US $)':'Date', 'Tesla Quarterly Revenue (Millions of US $).1':'Revenue'}, inplace=True)

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace('$',"")
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',',"")

tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

# print(tesla_revenue.head())

"""GAMESTOP"""

gme = yf.Ticker("GME")

gme_data = gme.history(period='max')

gme_data.reset_index(inplace=True)
# print(gme_data.head())

gme_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'

html_data = requests.get(gme_url).text
soup = BeautifulSoup(html_data, 'html5lib')

read_html_gme_data = pd.read_html(gme_url)
gme_revenue = read_html_gme_data[1]

# print(gme_revenue.columns)
gme_revenue.rename(columns={'GameStop Quarterly Revenue (Millions of US $)':'Date', 'GameStop Quarterly Revenue (Millions of US $).1':'Revenue'}, inplace=True)

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace('$',"")
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',',"")

gme_revenue.dropna(inplace=True)

gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

# print(gme_revenue.tail())

make_graph(tesla_data, tesla_revenue, 'Tesla')
make_graph(gme_data, gme_revenue, 'GameStop')