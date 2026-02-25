# Import required libraries
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX dataset
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get min and max payload values
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Create Dash app
app = dash.Dash(__name__)

# Get unique launch sites
launch_sites = spacex_df['Launch Site'].unique()

# Create layout
app.layout = html.Div(children=[

    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),

    # TASK 1: Dropdown for Launch Site
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in launch_sites],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie Chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: str(i) for i in range(0, 10001, 2000)},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # TASK 4: Scatter Plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback for Pie Chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):

    if entered_site == 'ALL':
        # Count total successful launches by site
        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
        return fig

    else:
        # Filter by selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

        # Count success and failure
        site_counts = filtered_df['class'].value_counts().reset_index()
        site_counts.columns = ['class', 'count']

        fig = px.pie(
            site_counts,
            values='count',
            names='class',
            title=f'Success vs Failure for {entered_site}'
        )
        return fig


# TASK 4: Callback for Scatter Plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_plot(selected_site, payload_range):

    low, high = payload_range

    # Filter payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs Launch Outcome for All Sites'
        )
        return fig

    else:
        site_df = filtered_df[
            filtered_df['Launch Site'] == selected_site
        ]

        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs Launch Outcome for {selected_site}'
        )
        return fig


# Run the app
if __name__ == '__main__':
    app.run()