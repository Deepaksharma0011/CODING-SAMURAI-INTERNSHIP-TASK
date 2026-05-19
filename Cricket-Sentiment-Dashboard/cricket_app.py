import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from textblob import TextBlob
import dash_bootstrap_components as dbc
import re

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Cricket Sentiment Dashboard"
server = app.server

# ── Sample Cricket Tweets Data ───────────────────────────────────────────────
cricket_data = {
    'India': [
        "India played brilliantly today! Rohit Sharma is absolutely amazing!",
        "What a fantastic innings by Virat Kohli! India dominates!",
        "India bowled out cheaply, very disappointing performance",
        "Bumrah is the best bowler in the world! India will win the series!",
        "India lost again, pathetic batting lineup",
        "Shubman Gill played a masterclass innings for India!",
        "India's fielding was terrible today, so many dropped catches",
        "India won the World Cup! Historic moment for Indian cricket!",
        "Very average performance by India, need to do better",
        "India's pace attack is world class, Bumrah and Siraj are unstoppable!",
        "Disappointed with India's batting collapse again",
        "India crushed Australia in the final, what a performance!",
        "India's top order failed miserably today",
        "Hardik Pandya played a match winning knock for India!",
        "India's bowling attack is the best in the world right now",
        "India struggled against spin today, need improvement",
        "What a stunning victory for India against England!",
        "India's fielding has improved a lot this series",
        "India lost the test series, very disappointing",
        "India vs Australia final was the best cricket match ever!",
    ],
    'Australia': [
        "Australia played some exceptional cricket today!",
        "Steve Smith is a genius, Australia will always fight back",
        "Australia collapsed badly, terrible batting performance",
        "Pat Cummins led Australia brilliantly in this series",
        "Australia's fielding is always top class, amazing effort",
        "Australia lost badly today, very poor showing",
        "Warner played an outstanding knock for Australia!",
        "Australia's bowling attack destroyed the opposition",
        "Australia played below par today, not their best",
        "Australia are the best team in the world right now!",
        "Australia's batting was inconsistent throughout the series",
        "What a brilliant bowling spell by Starc for Australia!",
        "Australia choked in the final, very disappointing",
        "Australia's aggressive brand of cricket is so exciting!",
        "Australia dominated the test match from start to finish",
        "Australia struggled in the subcontinent conditions",
        "Incredible comeback by Australia in the second innings!",
        "Australia's pace battery is the most feared in the world",
        "Australia played poorly in the powerplay overs",
        "Australia won the ashes again, cricket at its finest!",
    ],
    'England': [
        "England's Bazball cricket is so entertaining to watch!",
        "Stokes led England to an incredible victory today!",
        "England collapsed under pressure, very disappointing",
        "England's aggressive test cricket is revolutionizing the game",
        "Root played a magnificent century for England!",
        "England lost the series badly, need serious improvement",
        "England's bowling was exceptional in the first innings",
        "Brilliant leadership by Ben Stokes, England are back!",
        "England's batting lineup is inconsistent and unreliable",
        "England played some of the best cricket I have seen!",
        "England struggled against quality spin bowling today",
        "What a stunning chase by England, absolutely incredible!",
        "England's fielding was shocking today, cost them the match",
        "Anderson bowled beautifully for England as always",
        "England are playing fearless attacking cricket under Stokes",
        "England lost early wickets and never recovered",
        "Brilliant performance by England to win the test series!",
        "England's top order is their biggest weakness right now",
        "England vs Australia ashes was an absolute thriller!",
        "England played with great heart and determination today",
    ],
    'New Zealand': [
        "New Zealand play the most disciplined cricket in the world!",
        "Kane Williamson is the most complete batsman of his era",
        "New Zealand lost heartbreakingly in the final again",
        "New Zealand cricket team is always so professional",
        "Trent Boult bowled magnificently for New Zealand today",
        "New Zealand's batting was very ordinary in this match",
        "New Zealand are always competitive in every format",
        "What a classy innings by Kane Williamson for New Zealand!",
        "New Zealand lost to India in a close thriller",
        "New Zealand cricket has produced some amazing players",
    ],
    'Pakistan': [
        "Pakistan played some breathtaking cricket today!",
        "Babar Azam is one of the best batsmen in the world!",
        "Pakistan collapsed again, very inconsistent team",
        "Pakistan's pace attack with Shaheen is world class!",
        "Pakistan won an incredible match against India!",
        "Pakistan's batting order is too fragile and unreliable",
        "Shaheen Afridi is the best left arm pacer in cricket!",
        "Pakistan played brilliantly to qualify for the finals",
        "Pakistan lost a match they should have easily won",
        "Pakistan vs India is always the best cricket rivalry!",
    ]
}

def get_sentiment(text):
    score = TextBlob(text).sentiment.polarity
    if score > 0.1:
        return 'Positive', score
    elif score < -0.1:
        return 'Negative', score
    else:
        return 'Neutral', score

def analyze_team(tweets):
    results = [get_sentiment(t) for t in tweets]
    sentiments = [r[0] for r in results]
    scores = [r[1] for r in results]
    return {
        'Positive': sentiments.count('Positive'),
        'Negative': sentiments.count('Negative'),
        'Neutral':  sentiments.count('Neutral'),
        'avg_score': np.mean(scores),
        'tweets': tweets,
        'sentiments': sentiments
    }

# Pre-analyze all teams
team_analysis = {team: analyze_team(tweets) for team, tweets in cricket_data.items()}

TEAM_COLORS = {
    'India':       '#FF6B35',
    'Australia':   '#FFD700',
    'England':     '#00BFFF',
    'New Zealand': '#00C851',
    'Pakistan':    '#76FF03',
}

# ── Layout ────────────────────────────────────────────────────────────────────
app.layout = dbc.Container([

    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🏏 Cricket Team Sentiment Dashboard",
                    className="text-center fw-bold mt-4",
                    style={'color': '#FF6B35'}),
            html.P("Analyze Twitter Sentiment for Cricket Teams Worldwide",
                   className="text-center text-muted mb-4")
        ])
    ]),

    # Team selector
    dbc.Row([
        dbc.Col([
            dbc.Card([dbc.CardBody([
                html.Label("🏳️ Select Teams to Compare:", className="text-white fw-bold mb-2"),
                dcc.Checklist(
                    id='team-selector',
                    options=[{'label': f'  {t}', 'value': t} for t in cricket_data.keys()],
                    value=['India', 'Australia', 'England'],
                    inline=True,
                    className="text-white",
                    inputStyle={"margin-right": "6px", "margin-left": "15px"}
                )
            ])], color="dark", outline=True)
        ])
    ], className="mb-4"),

    # KPI Cards
    dbc.Row(id='kpi-cards', className="mb-4"),

    # Sentiment Comparison + Pie
    dbc.Row([
        dbc.Col([
            dbc.Card([dbc.CardBody([
                dcc.Graph(id='bar-chart', style={'height': '400px'})
            ])], color="dark", outline=True)
        ], width=7),

        dbc.Col([
            dbc.Card([dbc.CardBody([
                dcc.Dropdown(
                    id='pie-team',
                    options=[{'label': t, 'value': t} for t in cricket_data.keys()],
                    value='India',
                    clearable=False,
                    style={'color': 'black', 'marginBottom': '10px'}
                ),
                dcc.Graph(id='pie-chart', style={'height': '350px'})
            ])], color="dark", outline=True)
        ], width=5),
    ], className="mb-4"),

    # Sentiment Score + Tweet Table
    dbc.Row([
        dbc.Col([
            dbc.Card([dbc.CardBody([
                dcc.Graph(id='score-chart', style={'height': '350px'})
            ])], color="dark", outline=True)
        ], width=6),

        dbc.Col([
            dbc.Card([dbc.CardBody([
                html.H5("📝 Sample Tweets", className="text-white mb-3"),
                dcc.Dropdown(
                    id='tweet-team',
                    options=[{'label': t, 'value': t} for t in cricket_data.keys()],
                    value='India',
                    clearable=False,
                    style={'color': 'black', 'marginBottom': '10px'}
                ),
                html.Div(id='tweet-list', style={'maxHeight': '280px', 'overflowY': 'auto'})
            ])], color="dark", outline=True)
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


# ── Callbacks ─────────────────────────────────────────────────────────────────
@app.callback(
    [Output('kpi-cards', 'children'),
     Output('bar-chart', 'figure'),
     Output('score-chart', 'figure')],
    [Input('team-selector', 'value')]
)
def update_main(selected_teams):
    if not selected_teams:
        selected_teams = ['India']

    # KPI Cards
    kpi_cards = []
    for team in selected_teams:
        data   = team_analysis[team]
        total  = len(cricket_data[team])
        pos_pct = round(data['Positive'] / total * 100)
        score  = data['avg_score']
        mood   = "😊 Positive" if score > 0.1 else "😠 Negative" if score < -0.1 else "😐 Neutral"
        kpi_cards.append(
            dbc.Col(dbc.Card([dbc.CardBody([
                html.H6(team, className="fw-bold", style={'color': TEAM_COLORS.get(team, '#fff')}),
                html.H4(f"{pos_pct}% Positive", className="text-success"),
                html.P(f"Mood: {mood}", className="text-muted mb-0"),
                html.P(f"Score: {score:.2f}", className="text-muted mb-0"),
            ])], color="dark", outline=True), width=12 // max(len(selected_teams), 1))
        )

    # Bar chart
    fig_bar = go.Figure()
    for sentiment, color in [('Positive', '#00C851'), ('Neutral', '#FFD700'), ('Negative', '#FF4444')]:
        fig_bar.add_trace(go.Bar(
            name=sentiment,
            x=selected_teams,
            y=[team_analysis[t][sentiment] for t in selected_teams],
            marker_color=color
        ))
    fig_bar.update_layout(
        title='Sentiment Comparison by Team',
        barmode='group',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation='h', y=1.1)
    )

    # Score chart
    scores = [team_analysis[t]['avg_score'] for t in selected_teams]
    colors = ['#00C851' if s > 0.1 else '#FF4444' if s < -0.1 else '#FFD700' for s in scores]
    fig_score = go.Figure(go.Bar(
        x=selected_teams, y=scores,
        marker_color=colors,
        text=[f"{s:.3f}" for s in scores],
        textposition='outside'
    ))
    fig_score.update_layout(
        title='Average Sentiment Score by Team',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title='Sentiment Score (-1 to +1)'
    )

    return kpi_cards, fig_bar, fig_score


@app.callback(
    Output('pie-chart', 'figure'),
    Input('pie-team', 'value')
)
def update_pie(team):
    data   = team_analysis[team]
    labels = ['Positive', 'Negative', 'Neutral']
    values = [data['Positive'], data['Negative'], data['Neutral']]
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        marker_colors=['#00C851', '#FF4444', '#FFD700'],
        hole=0.4
    ))
    fig.update_layout(
        title=f'{team} Sentiment Breakdown',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig


@app.callback(
    Output('tweet-list', 'children'),
    Input('tweet-team', 'value')
)
def update_tweets(team):
    data      = team_analysis[team]
    tweets    = data['tweets']
    sentiments = data['sentiments']
    colors    = {'Positive': '#00C851', 'Negative': '#FF4444', 'Neutral': '#FFD700'}
    items = []
    for tweet, sentiment in zip(tweets[:8], sentiments[:8]):
        items.append(
            dbc.Card([dbc.CardBody([
                html.P(tweet, className="mb-1", style={'fontSize': '12px', 'color': 'white'}),
                dbc.Badge(sentiment, color="success" if sentiment == 'Positive'
                          else "danger" if sentiment == 'Negative' else "warning")
            ])], color="secondary", outline=True, className="mb-2")
        )
    return items


if __name__ == '__main__':
    app.run(debug=True)
