# Run as python qc_plotting_app.py
# Open http://127.0.0.1:8050/ in a web browser while its running

# The Json query file is currently pathed in a data folder from the directory this script is run (data/query.json)

# Import dash modules
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from string import ascii_uppercase
from plotly.subplots import make_subplots


# Import other modules
import plotly.graph_objects as go
# import plotly.express as px
# import pandas as pd
# import json
# import datetime as dt
import matplotlib.pyplot as plt



# App structure
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

alphabet = {num:i for num,i in zip(range(1,27),ascii_uppercase)}

fig = make_subplots(rows=5, cols=5)

for row_i in range(1,6):
    for col_i in range(1,6):
        fig.add_trace(
            go.Scatter(
                x=[1], y=[1],
                text=str([row_i,col_i]),
                mode="text",
            ),
            row=row_i, col=col_i
        )


fig.update_traces(
    textposition='middle center',
    textfont_size=20,
    showlegend=False,
    
)
fig.update_xaxes(showgrid=False,showticklabels=False)
fig.update_yaxes(showgrid=False,showticklabels=False)


#Subplot creating function
def create_subplot(row, col, fig, color="gray",text="hi"):
    fig.add_trace(
        go.Scatter(
            x=[1], y=[1],
            text=str(text),
            mode="text + markers",
            textfont = dict(color="Black",
                           size=20),
            marker = dict(color=color,
                          size = 50,
                          ),
            marker_symbol="star"

        ),
        row=row, col=col
    )
    
#Base subplot to make changes to
    #~ Color is defined by the marker 
fig = make_subplots(rows=6, cols=5)

fig = make_subplots(rows=6, cols=5)

for row_i in range(1,6):
    for col_i in range(1,6):
        create_subplot(row_i, col_i, fig, text = "")
        
fig.update_traces(
    textposition='middle center',
    showlegend=False,
)   

fig.update_xaxes(showgrid=False,showticklabels=False)
fig.update_yaxes(showgrid=False,showticklabels=False)


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~App layout~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##


app.layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.H3(
                    "Layout test",
                    style={
                        "font-size": "60px",
                        "margin-top": "5px",
                        "margin-bottom" : "0px",
                        "textAlign": "center",
                    },
                ),    
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id = "plots",
                    figure= fig
                ),
                width={"size": "10","offset":"1"},
                align="center",
                
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Input(
                    id = "input_box",
                    type="text",
                    maxlength=5,
                    placeholder="hello",
                    invalid=True,
                    # size="lg",
                    class_name="mb-3",
                    value=[],
                    pattern=r"[a-z]"
                ),
                width={"size": "4","offset":4},
                align="center",
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    id="text_output",
                    children="Enter a value",
                )
            )
        )
    ]
)

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Callbacks ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
#Define the word to guess somewhere
answer = list("lemon")


@app.callback(
    Output("plots", "figure"),
    Output("text_output", "children"),
    Input("input_box", "value"),
)

def update_plots(word):
    #Somewhere here it should recieve the plot to update rather than using the global plot 

    #Set the word to 5 letters 
    word = list(word)
    while len(word) <5:
        word.append("")
    
    for guess_letter, ans_letter, num in zip(word,answer,range(0,5)):
        fig.data[num].text = guess_letter
        # if guess_letter is ans_letter:
            # fig.data[num].marker.update(color="green")
        # elif guess_letter in answer:
            # fig.data[num].marker.update(color="yellow")
        # else:
            # fig.data[num].marker.update(color="grey")    
    # print(word)
    print(zip(word,answer,range(0,5)))
    return fig





















if __name__ == "__main__":
    app.run_server(debug=True)
