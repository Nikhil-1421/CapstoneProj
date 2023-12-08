# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=[
                                    {'label':'All Sites', 'value':'ALL'},
                                    {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                    {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                    {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                    {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                ],
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True
                                ),
                                html.Br(), 

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=min_payload,
                                    max=max_payload,
                                    step=500,
                                    marks={0:'0',800:'800',1600:'1600',2400:'2400',3200:'3200',4000:'4000',4800:'4800',5600:'5600',6400:'6400',7200:'7200',8000:'8000',8800:'8800',9600:'9600'},
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),])
                                

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')]
)
def gpc(entered_site):
    if entered_site == 'ALL':
        f_df = spacex_df.groupby(['Launch Site'])['class'].sum().reset_index()
        fig1=px.pie(f_df, values='class',names='Launch Site', title='All Launch Sites')
        return fig1
    else:
        s1=spacex_df[spacex_df['Launch Site'] == entered_site]
        s1_counts = s1['class'].value_counts().reset_index()
        s1_counts.columns = ['class','count']
        fig2=px.pie(s1_counts, values='count', names='class', title=f'Total Success Launches for site {entered_site}')
        return fig2



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)
def gsc(entered_site, selected_payload_mass):
    f2_df = spacex_df[spacex_df['Payload Mass (kg)'].between(selected_payload_mass[0], selected_payload_mass[1])]
    
    if entered_site == 'ALL':
        fig3 = px.scatter(f2_df, y='class', x='Payload Mass (kg)', color='Booster Version Category', title='All Launch Sites')
        return fig3
    else:
        s2 = f2_df[f2_df['Launch Site'] == entered_site]
        fig4 = px.scatter(s2, y='class', x='Payload Mass (kg)', color='Booster Version Category', title=f'Payload Correlation for {entered_site}')
        return fig4

# Run the app
if __name__ == '__main__':
    app.run_server()
