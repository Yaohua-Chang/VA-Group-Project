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
df = pd.read_csv('data/Data_vis_P.csv')
df2 = pd.read_csv('data/TurkishBMI.csv')

#the combination index generated from eating behaviors
df['com']=df['s_q8_1']+df['s_q8_2']-df['s_q7_1']-df['s_q7_3']  
                                                               

map_gender = {1: "male", 2: "female"}
df["gender"] = df["gender"].map(map_gender)

map_month = {1: "Jan.", 2: "Feb.", 3: "Mar.", 4: "Apr.", 5: "May", 6: "June", 7: "July", 8: "Aug.", 9: "Sept.", 10: "Oct.", 11: "Nov.", 12: "Dec."}
df["month_birth"] = pd.DatetimeIndex(pd.to_datetime(df["s_q6_date_birth"])).month.map(map_month)
domain_minths = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]

traces_com = [] 
for com in df.com.unique():
    traces_com.append(go.Violin(x=df['com'][df['com'] == com], y=df[df["com"] == com]["s_BMI"],name=str(com)))

traces_gender = []
for gender in df.gender.unique():
    traces_gender.append(go.Box(y=df[df["gender"] == gender]["s_BMI"],name=gender,marker={"size": 2}, boxpoints='all'))

traces_months = []
for month in df.month_birth.unique():
    traces_months.append(go.Box(y=df[df["month_birth"] == month]["s_BMI"],name=month, marker={"size": 2}, boxpoints='all'))

traces_income = []
income_range = ["0", "<1000", "<2000", "<3000", "<5000", "<7000", "<=9999", ">9999"]
healthy_range = ['Underweight','Overweight','Obese', 'Healthy']
color_range = ['green', 'red','yellow','blue']

traces_income.append(go.Bar(x=income_range, y=[0, 0, 7, 2, 2, 1, 1, 1],  name=healthy_range[0]))
traces_income.append(go.Bar(x=income_range, y=[1, 10, 32, 14, 9, 3, 1, 1], name=healthy_range[1]))
traces_income.append(go.Bar(x=income_range, y=[0, 5, 29, 20, 4, 5, 0, 1], name=healthy_range[2]))
traces_income.append(go.Bar(x=income_range, y=[8, 55, 86, 51, 34, 9, 7, 1], name=healthy_range[3]))

traces_income_percent = []
traces_income_percent.append(go.Bar(y=income_range, x=[0.0, 0.0, 4.55, 2.3, 4.08, 5.56, 11.11, 25.0], name=healthy_range[0],
  orientation='h'))
traces_income_percent.append(go.Bar(y=income_range, x=[11.11, 14.29, 20.78, 16.09, 18.37, 16.67, 11.11, 25.0], name=healthy_range[1],
  orientation='h'))
traces_income_percent.append(go.Bar(y=income_range, x=[0.0, 7.14, 18.83, 22.99, 8.16, 27.78, 0.0, 25.0], name=healthy_range[2],
  orientation='h'))
traces_income_percent.append(go.Bar(y=income_range, x= [88.89, 78.57, 55.84, 58.62, 69.39, 50.0, 77.78, 25.0], name=healthy_range[3],
  orientation='h'))

app.layout = html.Div([html.Div([
        html.H1("The Study for Obesity of Students in Turkey")], style={"textAlign": "center"}),
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
        ),
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
                                margin={"l": 200, "b": 100, "r": 200},
                                xaxis={'categoryorder':'array', 'categoryarray':domain_minths},
                                yaxis={"title": "BMI"})}
        ),
        dcc.Graph(
            id="income-graph",
            figure={
                "data": traces_income,
                "layout": go.Layout(title=f"BMI VS. income",autosize=True,
                                barmode='stack',
                                margin={"l": 200, "b": 100, "r": 200},
                                xaxis={"title": "Monthly Income","showticklabels": True},
                                yaxis={"title": "Count of Records"})}
        ),
        dcc.Graph(
            id="income-percent-graph",
            figure={
                "data": traces_income_percent,
                "layout": go.Layout(title=f"BMI VS. income",autosize=True,
                                barmode='stack',
                                margin={"l": 200, "b": 100, "r": 200},
                                xaxis={"title": "Percentage of BMI per Incone Level(%)","showticklabels": True},
                                yaxis={"title": "Monthly Income"})}
        ),
], className="container")


if __name__ == "__main__":
    app.run_server(debug=True)