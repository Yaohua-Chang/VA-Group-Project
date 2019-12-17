# -*- coding: utf-8 -*-
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from plotly.colors import n_colors

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Load data
df = pd.read_csv('data/Data_vis_P.csv')
df2 = pd.read_csv('data/TurkishBMI.csv')

# The combination index generated from eating behaviors
df['com']=df['s_q8_1']+df['s_q8_2']-df['s_q7_1']-df['s_q7_3']  

def compute_health_status(row):
    if row['s_BMI'] < 14:
        return "Underweight"
    elif 14 <= row['s_BMI'] <= 19:
        return 'Healthy'
    elif 19 < row['s_BMI'] <= 21.5:
        return 'Overweight'    
    elif row['s_BMI'] > 21.5:
        return 'Obese'  

df['health_status'] = df.apply(lambda row: compute_health_status(row), axis=1)

map_gender = {1: "Male", 2: "Female"}
df["gender"] = df["gender"].map(map_gender)

map_month = {1: "Jan.", 2: "Feb.", 3: "Mar.", 4: "Apr.", 5: "May", 6: "June", 7: "July", 8: "Aug.", 9: "Sept.", 10: "Oct.", 11: "Nov.", 12: "Dec."}
df["month_birth"] = pd.DatetimeIndex(pd.to_datetime(df["s_q6_date_birth"])).month.map(map_month)
domain_months = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]

gender_indicators = ["All Genders", "Male", "Female"]
months_indicators = ["All Months", "Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
health_indicators = ["All Health Status", 'Underweight','Overweight','Obese', 'Healthy']

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

motherBmi = []
fatherBmi = []
for idex, row in df.iterrows():
    motherBmi.append((row['q5']/((row['q6']/100)**2)))
    fatherBmi.append((row['q11']/((row['q12']/100)**2)))
df['Mother_BMI'] = motherBmi
df['Father_BMI'] = fatherBmi

colors = n_colors('rgb(0, 100, 255)', 'rgb(0, 10, 0)', 6, colortype='rgb')
values = [-1, 0, 1, 2, 3, 4]

app.layout = html.Div([
        html.Div([
            html.H1("The Study for Obesity of Students in Turkey"),

            html.Div([
                dcc.Dropdown(
                    id='crossfilter-gender',
                    options=[{'label': i, 'value': i} for i in gender_indicators],
                    value='All Genders'
                )
            ], style={'width': '30%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-month',
                    options=[{'label': i, 'value': i} for i in months_indicators],
                    value='All Months'
                )
            ], style={'width': '30%', 'display': 'inline-block','margin': '0px 20px'}),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-health',    
                    options=[{'label': i, 'value': i} for i in health_indicators],
                    value='All Health Status'
                )
            ], style={'width': '30%', 'display': 'inline-block'}),
        ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px',
        "textAlign": "center",
        "position": "fixed",
        "top": "0",
        "width": "100%",
        "z-index":"9"
        }),

        html.Div([
            dcc.Graph(
                id="eating-graph"
            ),

            dcc.Graph(
                id="gender-graph"
            ),

            dcc.Graph(
                id="months-graph"
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

            dcc.Graph(
                id="parents-graph"
            ),
        ], style={"padding": '200px 0px', "height": "2000px"})

        # html.Div([
        #     html.Img(
        #         id="parents-graph-img",
        #         src="assets/Picture1.png"
        #         )], 
        #     style={"textAlign": "center"}),
        
], className="container")

@app.callback(
    Output('eating-graph', 'figure'),
    [Input('crossfilter-gender', 'value'),
    Input('crossfilter-month', 'value'),
    Input('crossfilter-health', 'value')])
def update_gender_graph(gender_type, month_type, health_type):
    traces_com = []
    df_select = df
    if gender_type != "All Genders":
        df_select = df[df["gender"] == gender_type]

    if month_type != "All Months":
        df_select = df_select[df_select["month_birth"] == month_type]

    if health_type != "All Health Status":
        df_select = df_select[df_select["health_status"] == health_type]

    for com, color in zip(values, colors):
        traces_com.append(go.Violin(x=df_select['com'][df_select['com'] == com], y=df_select[df_select["com"] == com]["s_BMI"],name=str(com), line={"color":color}))

    return {
        "data": traces_com,
        "layout": go.Layout(title=f"BMI VS. Eating Behaviors",
                        autosize=True,
                        showlegend=False,
                        margin={"l": 200, "b": 100, "r": 200},
                        xaxis={"title": "vegetable & fruit  <----------------->  beverage & chips"},
                        yaxis={"title": "BMI"})
    }


@app.callback(
    Output('gender-graph', 'figure'),
    [Input('crossfilter-gender', 'value'),
    Input('crossfilter-month', 'value'),
    Input('crossfilter-health', 'value')])
def update_gender_graph(gender_type, month_type, health_type):
    traces_gender = []
    df_select = df
    if gender_type != "All Genders":
        df_select = df[df["gender"] == gender_type]

    if month_type != "All Months":
        df_select = df_select[df_select["month_birth"] == month_type]

    if health_type != "All Health Status":
        df_select = df_select[df_select["health_status"] == health_type]

    for gender in df_select.gender.unique():
            traces_gender.append(go.Box(y=df_select[df_select["gender"] == gender]["s_BMI"],name=gender,marker={"size": 2}, boxpoints='all', jitter=0.3, ))
    
    return {
        "data": traces_gender,
        "layout": go.Layout(title=f"BMI VS. Gender",autosize=True,
                        margin={"l": 200, "b": 100, "r": 200},xaxis={"showticklabels": True},
                        yaxis={"title": "BMI"})
    }


@app.callback(
    Output('months-graph', 'figure'),
    [Input('crossfilter-gender', 'value'),
    Input('crossfilter-month', 'value'),
    Input('crossfilter-health', 'value')])
def update_month_graph(gender_type, month_type, health_type):
    traces_months = []
    df_select = df
    if gender_type != "All Genders":
        df_select = df[df["gender"] == gender_type]

    if month_type != "All Months":
        df_select = df_select[df_select["month_birth"] == month_type]

    if health_type != "All Health Status":
        df_select = df_select[df_select["health_status"] == health_type]

    for month in df_select.month_birth.unique():
        traces_months.append(go.Box(y=df_select[df_select["month_birth"] == month]["s_BMI"],name=month, marker={"size": 2}, boxpoints='all',jitter=0.3))

    return {
        "data": traces_months,
        "layout": go.Layout(title=f"BMI VS. Month",autosize=True,
                        margin={"l": 200, "b": 100, "r": 200},
                        xaxis={'categoryorder':'array', 'categoryarray':domain_months},
                        yaxis={"title": "BMI"})
    }

@app.callback(
    Output('parents-graph', 'figure'),
    [Input('crossfilter-gender', 'value'),
    Input('crossfilter-month', 'value'),
    Input('crossfilter-health', 'value')])
def update_parent_graph(gender_type, month_type, health_type):
    traces_parents = []
    df_select = df
    if gender_type != "All Genders":
        df_select = df[df["gender"] == gender_type]

    if month_type != "All Months":
        df_select = df_select[df_select["month_birth"] == month_type]

    if health_type != "All Health Status":
        df_select = df_select[df_select["health_status"] == health_type]


    traces_parents.append(go.Box(y=df_select["s_BMI"],name="Student BMI", marker={"size": 2}, boxpoints='all',jitter=0.3))
    traces_parents.append(go.Box(y=df_select["Mother_BMI"],name="Mother BMI", marker={"size": 2}, boxpoints='all',jitter=0.3))
    traces_parents.append(go.Box(y=df_select["Father_BMI"],name="Father BMI", marker={"size": 2}, boxpoints='all',jitter=0.3))

    return {
        "data": traces_parents,
        "layout": go.Layout(title=f"BMI VS. Parents",autosize=True,
                        margin={"l": 200, "b": 100, "r": 200},
                        xaxis={'categoryorder':'array', 'categoryarray':domain_months},
                        yaxis={"title": "BMI"})
    }
    
if __name__ == "__main__":
    app.run_server(debug=True)