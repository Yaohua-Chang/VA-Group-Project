# -*- coding: utf-8 -*-
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Load data
df = pd.read_csv('data/Cleaned10_23.csv')
df["s_BMI"] = df["s_weight"] / (df["s_height"] / 100)**2

#the combination index generated from eating behaviors
df['com']=df['s_q8_1']+df['s_q8_2']-df['s_q7_1']-df['s_q7_3']  
                                                               

map_gender = {1: "male", 2: "female"}
df["gender"] = df["gender"].map(map_gender)

map_month = {1: "Jan.", 2: "Feb.", 3: "Mar.", 4: "Apr.", 5: "May", 6: "June", 7: "July", 8: "Aug.", 9: "Sept.", 10: "Oct.", 11: "Nov.", 12: "Dec."}
df["month_birth"] = pd.DatetimeIndex(pd.to_datetime(df["s_q6_date_birth"])).month.map(map_month)

traces_gender = []
for gender in df.gender.unique():
    traces_gender.append(go.Box(y=df[df["gender"] == gender]["s_BMI"],name=gender,marker={"size": 2}, boxpoints='all'))

traces_months = []
for month in df.month_birth.unique():
    traces_months.append(go.Box(y=df[df["month_birth"] == month]["s_BMI"],name=month, marker={"size": 2}, boxpoints='all'))

traces_com = [] 
for com in df.com.unique():
    traces_com.append(go.Violin(x=df['com'][df['com'] == com], y=df[df["com"] == com]["s_BMI"],name=str(com)))

app.layout = html.Div([html.Div([
        html.H1("The Study for Obesity of Students in Turkey")], style={"textAlign": "center"}),
        dcc.Graph(
            id="gender-graph",
            figure={
                "data": traces_gender,
                "layout": go.Layout(title=f"BMI VS. Gender",autosize=True,
                                margin={"l": 200, "b": 100, "r": 200},xaxis={"showticklabels": True},
                                yaxis={"title": "BMI"})}
        ),
        dcc.Graph(
            id="months-graph",
            figure={
                "data": traces_months,
                "layout": go.Layout(title=f"BMI VS. Month",autosize=True,
                                margin={"l": 200, "b": 100, "r": 200},xaxis={"showticklabels": True},
                                yaxis={"title": "BMI"})}
        ),
        dcc.Graph(
            id="com-graph",
            figure={
                "data": traces_com,
                "layout": go.Layout(title=f"BMI VS. Eating Behaviors",
                                autosize=True,
                                showlegend=False,
                                margin={"l": 200, "b": 100, "r": 200},
                                xaxis={"title": "vegetable & fruit  <----------------->  beverage & chips"},
                                yaxis={"title": "BMI"})}
        )
], className="container")


if __name__ == "__main__":
    app.run_server(debug=True)