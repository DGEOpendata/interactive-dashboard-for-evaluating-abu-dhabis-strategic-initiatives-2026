python
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load dataset
data_url = "https://data.abudhabi.gov.ae/dataset/2026-sub-awards-nomination-open-data.xlsx"
df = pd.read_excel(data_url)

# Example data cleaning
df['Actual Budget'] = df['Actual Budget'].fillna(0)

# Create Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Evaluation of Joint Initiatives Aligned with Abu Dhabi Government's Strategic Objectives"),
    dcc.Dropdown(
        id='initiative-dropdown',
        options=[{'label': initiative, 'value': initiative} for initiative in df['Initiative Name'].unique()],
        placeholder="Select an Initiative"
    ),
    dcc.Graph(id='budget-vs-benefits-chart')
])

@app.callback(
    dash.dependencies.Output('budget-vs-benefits-chart', 'figure'),
    [dash.dependencies.Input('initiative-dropdown', 'value')]
)
def update_chart(selected_initiative):
    filtered_df = df if not selected_initiative else df[df['Initiative Name'] == selected_initiative]
    fig = px.bar(
        filtered_df,
        x='Initiative Name',
        y=['Planned Budget', 'Actual Budget'],
        title='Planned vs Actual Budget'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
