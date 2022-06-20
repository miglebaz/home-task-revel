from dash import Dash, html, dcc
import os
import plotly.express as px
import pandas as pd

app = Dash(__name__)

colors = {
    'background': '#d3d3d3',
    'featured': '#00a3e0',
    'text': '#212121'
}

case_df = pd.read_csv('data/cs_data.csv')
case_df["Platform"].fillna("No Platform", inplace=True)
case_df['Date/Time Solved (PST)'] = pd.to_datetime(case_df['Date/Time Solved (PST)'])


fig = px.histogram(
    case_df, x="Platform", color='Feature',
    title='Platform distribution'
)

training_provided_data = case_df.loc[case_df['Closure Code'] == 'Advice/Training provided']
fig2 = px.histogram( training_provided_data, x="Reason Code", barmode="group",  color='Type',
                     title='Reason Code distribution where advice/training was provided')


cases_count_by_weekday = case_df["Date/Time Solved (PST)"].dt.weekday.value_counts()
cases_count_by_hour_of_day = case_df["Date/Time Solved (PST)"].dt.hour.value_counts()
fig3 = px.bar(case_df, x=cases_count_by_hour_of_day.index, y=cases_count_by_hour_of_day.values, barmode="group",
              title='Number of cases solved during hours of the day',
              labels=dict(x="Time Solved (PST)", y="Number of cases")
              )

weekdays = ['Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
fig4 = px.bar(case_df, x=weekdays, y=cases_count_by_weekday.values, barmode="group",
              title='Number of cases solved during weekdays ',
              labels=dict(x="Weekday", y="Number of cases")
              )

fig5 = px.histogram(case_df, x ='Feature', title='Number of cases by feature', color='Reason Code')

app.layout = html.Div(children=[
    html.H1(children='Revel Home Task'),

    html.Div([
        html.Strong('3 major areas of product improvement Revel product team should focus on'),
        html.Ul([
            html.Li('Hardware / Networking'),
            html.Li('Management Console'),
            html.Li('POS'),
        ])
    ]),

    dcc.Graph(
        id='graph',
        figure=fig
    ),

    html.Div([
        html.Strong('2 training videos that customer training team should create ASAP:'),
        html.Ul([
            html.Li('How to activate/deactivate/delete'),
            html.Li('How to initial setup guidance'),
        ])
    ]),

    dcc.Graph(
        id='graph2',
        figure=fig2
    ),

    html.Div([
        html.Strong('There is a clear trend in the hours of the day that most agents should be working/on line:'),
        html.Ul([
            html.Li('Between 7 - 16 (PST)'),
            html.Li('The lowest number of cases are received appears to be on Sunday and Saturday, '
                    'so less agents should work on weekends '),
        ])
    ]),

    dcc.Graph(
        id='graph3',
        figure=fig3
    ),

    dcc.Graph(
        id='graph4',
        figure=fig4
    ),

    html.Div([
        html.Strong('At times when there are high volume of client requests coming,'
                    ' you have an idea how CS TS team should prioritise tickets:'),
        html.Ul([
            html.Li('Everything that is related with payments'),
        ])
    ]),

    dcc.Graph(
        id='graph5',
        figure=fig5
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)