import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import yfinance as yf
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "TCS Stock Dashboard"
server = app.server

# ── Layout ──────────────────────────────────────────────────────────────────
app.layout = dbc.Container([

    # Header
    dbc.Row([
        dbc.Col([
            html.H1("TCS Stock Analysis | Deepak Sharma",
                    className="text-center text-primary fw-bold mt-4"),
            html.P("Real-time TCS (Tata Consultancy Services) Stock Analysis",
                   className="text-center text-muted mb-4")
        ])
    ]),

    # Controls
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("📅 Select Time Period:", className="text-white fw-bold"),
                    dcc.Dropdown(
                        id='period-dropdown',
                        options=[
                            {'label': '1 Month',  'value': '1mo'},
                            {'label': '3 Months', 'value': '3mo'},
                            {'label': '6 Months', 'value': '6mo'},
                            {'label': '1 Year',   'value': '1y'},
                            {'label': '2 Years',  'value': '2y'},
                            {'label': '5 Years',  'value': '5y'},
                        ],
                        value='1y',
                        clearable=False,
                        style={'color': 'black'}
                    )
                ])
            ], color="dark", outline=True)
        ], width=4),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("📊 Chart Type:", className="text-white fw-bold"),
                    dcc.Dropdown(
                        id='chart-type',
                        options=[
                            {'label': 'Candlestick', 'value': 'candlestick'},
                            {'label': 'Line Chart',  'value': 'line'},
                        ],
                        value='candlestick',
                        clearable=False,
                        style={'color': 'black'}
                    )
                ])
            ], color="dark", outline=True)
        ], width=4),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("📉 Moving Average:", className="text-white fw-bold"),
                    dcc.Checklist(
                        id='ma-checklist',
                        options=[
                            {'label': ' 20 Day MA', 'value': 'MA20'},
                            {'label': ' 50 Day MA', 'value': 'MA50'},
                            {'label': ' 200 Day MA', 'value': 'MA200'},
                        ],
                        value=['MA20', 'MA50'],
                        inline=True,
                        className="text-white"
                    )
                ])
            ], color="dark", outline=True)
        ], width=4),
    ], className="mb-4"),

    # KPI Cards
    dbc.Row(id='kpi-cards', className="mb-4"),

    # Main Chart
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='main-chart', style={'height': '500px'})
                ])
            ], color="dark", outline=True)
        ])
    ], className="mb-4"),

    # Volume + Returns
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='volume-chart', style={'height': '300px'})
                ])
            ], color="dark", outline=True)
        ], width=6),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='returns-chart', style={'height': '300px'})
                ])
            ], color="dark", outline=True)
        ], width=6),
    ], className="mb-4"),

    # Footer
    dbc.Row([
        dbc.Col([
            html.P("Deepak Sharma | B.Tech AI & Data Science | Coding Samurai Internship",
                   className="text-center text-muted mt-2 mb-4")
        ])
    ])

], fluid=True)


# ── Callbacks ────────────────────────────────────────────────────────────────
@app.callback(
    [Output('kpi-cards', 'children'),
     Output('main-chart', 'figure'),
     Output('volume-chart', 'figure'),
     Output('returns-chart', 'figure')],
    [Input('period-dropdown', 'value'),
     Input('chart-type', 'value'),
     Input('ma-checklist', 'value')]
)
def update_dashboard(period, chart_type, ma_list):
    # Fetch data
    df = yf.download('TCS.NS', period=period)
    df.columns = df.columns.get_level_values(0)
    df = df.reset_index()

    # Moving averages
    df['MA20']  = df['Close'].rolling(20).mean()
    df['MA50']  = df['Close'].rolling(50).mean()
    df['MA200'] = df['Close'].rolling(200).mean()

    # Daily returns
    df['Returns'] = df['Close'].pct_change() * 100

    # ── KPI Cards ─────────────────────────────────────────────────────────
    current_price = float(df['Close'].iloc[-1])
    prev_price    = float(df['Close'].iloc[-2])
    change        = current_price - prev_price
    change_pct    = (change / prev_price) * 100
    high_52w      = float(df['High'].max())
    low_52w       = float(df['Low'].min())
    avg_volume    = int(df['Volume'].mean())

    color = "success" if change >= 0 else "danger"
    arrow = "▲" if change >= 0 else "▼"

    kpi_cards = [
        dbc.Col(dbc.Card([dbc.CardBody([
            html.H6("Current Price", className="text-muted"),
            html.H3(f"₹{current_price:,.2f}", className="text-white"),
            html.P(f"{arrow} ₹{abs(change):.2f} ({change_pct:+.2f}%)",
                   className=f"text-{color} mb-0")
        ])], color="dark", outline=True), width=3),

        dbc.Col(dbc.Card([dbc.CardBody([
            html.H6("52W High", className="text-muted"),
            html.H3(f"₹{high_52w:,.2f}", className="text-success"),
            html.P("Highest Price", className="text-muted mb-0")
        ])], color="dark", outline=True), width=3),

        dbc.Col(dbc.Card([dbc.CardBody([
            html.H6("52W Low", className="text-muted"),
            html.H3(f"₹{low_52w:,.2f}", className="text-danger"),
            html.P("Lowest Price", className="text-muted mb-0")
        ])], color="dark", outline=True), width=3),

        dbc.Col(dbc.Card([dbc.CardBody([
            html.H6("Avg Volume", className="text-muted"),
            html.H3(f"{avg_volume:,}", className="text-info"),
            html.P("Shares/Day", className="text-muted mb-0")
        ])], color="dark", outline=True), width=3),
    ]

    # ── Main Chart ────────────────────────────────────────────────────────
    fig_main = go.Figure()

    if chart_type == 'candlestick':
        fig_main.add_trace(go.Candlestick(
            x=df['Date'], open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name='TCS'
        ))
    else:
        fig_main.add_trace(go.Scatter(
            x=df['Date'], y=df['Close'],
            name='Close Price', line=dict(color='#00d4ff', width=2)
        ))

    # Moving averages
    ma_colors = {'MA20': 'orange', 'MA50': 'yellow', 'MA200': 'red'}
    for ma in (ma_list or []):
        fig_main.add_trace(go.Scatter(
            x=df['Date'], y=df[ma],
            name=ma, line=dict(color=ma_colors[ma], width=1.5, dash='dash')
        ))

    fig_main.update_layout(
        title='TCS Stock Price',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_rangeslider_visible=False,
        legend=dict(orientation='h', y=1.1)
    )

    # ── Volume Chart ──────────────────────────────────────────────────────
    vol_colors = ['#ef5350' if c < o else '#26a69a'
                  for c, o in zip(df['Close'], df['Open'])]

    fig_vol = go.Figure(go.Bar(
        x=df['Date'], y=df['Volume'],
        marker_color=vol_colors, name='Volume'
    ))
    fig_vol.update_layout(
        title='Trading Volume',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    # ── Returns Chart ─────────────────────────────────────────────────────
    fig_ret = go.Figure(go.Histogram(
        x=df['Returns'].dropna(),
        nbinsx=50,
        marker_color='#00d4ff',
        opacity=0.75,
        name='Daily Returns'
    ))
    fig_ret.update_layout(
        title='Daily Returns Distribution',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Return (%)',
        yaxis_title='Frequency'
    )

    return kpi_cards, fig_main, fig_vol, fig_ret


if __name__ == '__main__':
    app.run(debug=True)
