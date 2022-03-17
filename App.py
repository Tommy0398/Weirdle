# Run as python qc_plotting_app.py
# Open http://127.0.0.1:8050/ in a web browser while its running

# The Json query file is currently pathed in a data folder from the directory this script is run (data/query.json)

# Import dash modules
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from string import ascii_uppercase
from plotly.subplots import make_subplots
from dash.exceptions import PreventUpdate


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

# alphabet = {num:i for num,i in zip(range(1,27),ascii_uppercase)}

#Subplot creating function
def create_subplot(row, col, fig, color="gray",text="hi"):
    fig.add_trace(
        go.Scatter(
            x=[1], y=[1],
            text=str(text),
            mode="text + markers",
            textfont = dict(color="Black",
                           size=30),
            marker = dict(color=color,
                          size = 50,
                          opacity=0.6
                          ),
            marker_symbol="star",
            # marker_line_width=1

        ),
        row=row, col=col
    )
    
#Base subplot to make changes to
    #~ Color is defined by the marker 
fig = make_subplots(rows=6,
                    cols=5,
                    horizontal_spacing=0.01,
                    vertical_spacing=0.03,
        )

for row_i in range(1,7):
    for col_i in range(1,6):
        create_subplot(row_i, col_i, fig, text = " ")
        
fig.update_traces(
    textposition='middle center',
    showlegend=False,
)   

fig.update_xaxes(showgrid=False,showticklabels=False)
fig.update_yaxes(showgrid=False,showticklabels=False)
fig.update_layout(
    height=400,
    width=1000,
    margin=dict(
    l=200,
    r=0,
    b=10,
    t=10,
#                         pad=2
    )
)

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~App layout~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##


app.layout = dbc.Container(
    [
        #Row 1
        dbc.Row(
            dbc.Col(
                html.H3(
                    "Layout test",
                    style={
                        "font-size": "60px",
                        "margin-top": "5px",
                        "margin-bottom" : "5px",
                        "textAlign": "center",
                    },
                ),    
            )
        ),
        #Row 2
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id = "plots",
                    figure= fig,
                ),
                width={"size": "12","offset": "1"},
                align="center",
                
            ), 
            align = "center",
            justify = "center",
        ),
        #Row 3
        dbc.Row(
            [
                dbc.Col(
                    dbc.Input(
                        id = "input_box",
                        type="text",
                        maxlength=5,
                        placeholder="hello",
                        invalid=False,
                        class_name="mb-3",
                        value=[],
                    ),
                    width={"size": "4"},
                    align="center",
                ),
                dbc.Col(
                    dbc.Button(
                        "Enter",
                        id = "enter_button",
                        color="primary",
                        class_name= "mb-3",
                        size = "lg",
                        n_clicks = 0,
                    ),
                    width={"size": "2"},
                    align= "center",
                
                
                
                ),
            ],
            align="center",
            justify="center"
        ),
        #Row 4
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        id="text_output",
                        children="Enter a value",
                    ),
                ),
                dbc.Col(
                    dcc.Store(id="plot_store"),
                ),
            ],
            align="center",
            justify="center"
        ),
    ], 
    fluid=True
)

def update_plot_guess(word,answer,plot,range=range(0,5)):
    for guess_letter, ans_letter, num in zip(word,answer,range):
        #Add letter to graphs
        plot["data"][num]["text"] = guess_letter
        
        #Correct letter and postion
        if guess_letter == ans_letter:
            plot["data"][num]["marker"].update(color="green",symbol = "star")
            
        #Correct letter wrong position
        elif guess_letter in answer:
            plot["data"][num]["marker"].update(color="orange",symbol = "diamond")
            
        #Wrong letter and position
        else:
            plot["data"][num]["marker"].update(color="grey",symbol="x")
    
    return plot

def update_plot_input(word,answer,plot,range=range(0,5)):
    for guess_letter, ans_letter, num in zip(word,answer,range):
        #Add letter to graphs
        plot["data"][num]["text"] = guess_letter
            
    return plot



##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Callbacks ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
#Define the word to guess somewhere
answer = list("LEMON")

@app.callback(
    Output("plots", "figure"),
    Output("text_output", "children"),
    Input("input_box", "value"),
    State("enter_button", "n_clicks"),
    State("plot_store", "data"),
)

def update_plots(word,n_clicks,figure):
    #Somewhere here it should recieve the plot to update rather than using the global plot 
        #~ Temporaraly explicitly defining the plot as global to prevent an odd lag in inputs otherwise
        #~ Nevermind that isn't what was causing it. Just make sure the word.append isn't empty
    # global fig
    # fig = fig
        
    if figure == None:
        figure = fig
        
    #Set the word to 5 letters 
    word = list(word)
    while len(word) <5:
        word.append(" ")
    word = [x.upper() for x in word]
    
    #Add the letters to the plot and indicate whether the letters are correct
        #~ The correctness check needs to go into a different callback that utilises and input button(or other)
        #~ Also needs a bit more logic to account for letters occuring multiple times
        
    #Update the plot depending on the current input and guess count
    
    if n_clicks == 0:
        update_plot_input(word,answer,figure,range(0,5))
        
    if n_clicks == 1:
        update_plot_input(word,answer,figure,range(5,10))   

    if n_clicks == 2:
        update_plot_input(word,answer,figure,range(10,15))

    if n_clicks == 3:
        update_plot_input(word,answer,figure,range(15,20))
        
    if n_clicks == 4:
        update_plot_input(word,answer,figure,range(20,25))
        

        # if guess_letter == ans_letter:
            # figure["data"][num]["marker"].update(color="green",symbol = "star")
        # #Correct letter wrong position
        # elif guess_letter in answer:
            # figure["data"][num]["marker"].update(color="orange",symbol = "diamond")
        # #Wrong letter and position
        # else:
            # figure["data"][num]["marker"].update(color="grey",symbol="x")
            
    # print(dash.callback_context.triggered)     
            
            
    return figure, word


@app.callback(
    Output("plot_store", "data"),
    Input("enter_button", "n_clicks"),
    State("input_box", "value"),
    State("plots", "figure"),

)

def update_store(n_clicks,word,figure):


    if figure == None:
        figure = fig

    #Set the word to 5 letters 
    word = list(word)
    while len(word) <5:
        word.append(" ")
    word = [x.upper() for x in word]
    
    
    #Update the plot depending on the current guess
    
    if n_clicks == 1:
        update_plot_guess(word,answer,figure,range(0,5))
        
    if n_clicks == 2:
        update_plot_guess(word,answer,figure,range(5,10))   

    if n_clicks == 3:
        update_plot_guess(word,answer,figure,range(10,15))

    if n_clicks == 4:
        update_plot_guess(word,answer,figure,range(15,20))
        
    if n_clicks == 5:
        update_plot_guess(word,answer,figure,range(20,25))
        
        
    return figure


# # # # # def func(word,answer,plot,range=range(0,5)):
    # # # # # for guess_letter, ans_letter, num in zip(word,answer,range):
        # # # # # #Add letter to graphs
        # # # # # # figure["data"][num]["text"] = guess_letter
        # # # # # #Correct letter and postion
        
        # # # # # if guess_letter == ans_letter:
            # # # # # plot["data"][num]["marker"].update(color="green",symbol = "star")
        # # # # # #Correct letter wrong position
        # # # # # elif guess_letter in answer:
            # # # # # plot["data"][num]["marker"].update(color="orange",symbol = "diamond")
        # # # # # #Wrong letter and position
        # # # # # else:
            # # # # # plot["data"][num]["marker"].update(color="grey",symbol="x")
    
    # # # # # return plot













if __name__ == "__main__":
    app.run_server(debug=True)
