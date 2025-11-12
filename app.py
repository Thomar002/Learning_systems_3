import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Literal Automaton – Stationary Distribution", 
            style={"textAlign": "center", "color": "#2c3e50", "margin": "20px"}),
    
    html.Div([
        html.Div([
            html.Label("s (forgetting rate): 1.0 → 25.0"),
            dcc.Slider(id="s-slider", min=1, max=25, step=0.1, value=10,
                      marks={1: "1", 10: "10", 25: "25"}, tooltip={"placement": "bottom"}),
            
            html.Label("P(L|Y) – prob. of seeing letter when expected"),
            dcc.Slider(id="ply-slider", min=0, max=1, step=0.01, value=0.9,
                      marks={0: "0", 0.5: "0.5", 1: "1"}),
            
            html.Label("P(Y) – base rate of the letter"),
            dcc.Slider(id="py-slider", min=0, max=1, step=0.01, value=0.1,
                      marks={0: "0", 0.5: "0.5", 1: "1"}),
            
            html.Div(id="pliy-output", style={"margin": "20px 0", "fontSize": 18, "fontWeight": "bold"}),
        ], style={"width": "45%", "display": "inline-block", "verticalAlign": "top", "padding": "20px"}),
        
        dcc.Graph(id="bar-chart", style={"width": "50%", "display": "inline-block"})
    ])
])

@app.callback(
    Output("bar-chart", "figure"),
    Output("pliy-output", "children"),
    Input("s-slider", "value"),
    Input("ply-slider", "value"),
    Input("py-slider", "value")
)
def update_chart(s, P_L_given_Y, P_Y):
    P_notL_given_Y = 1 - P_L_given_Y
    P_notY = 1 - P_Y
    q = P_L_given_Y * P_Y + P_notL_given_Y * P_notY
    
    # === YOUR 8 UNNORMALIZED WEIGHTS ===
    w1 = P_Y**4
    w2 = P_Y**3 * P_notL_given_Y**6 * s * q
    w3 = P_Y**2 * P_notL_given_Y**5 * s**2 * q**2
    w4 = P_Y**1 * P_notL_given_Y**4 * s**3 * q**3
    w5 =            P_notL_given_Y**3 * s**4 * q**4
    w6 = P_L_given_Y * P_notL_given_Y**2 * s**5 * q**4
    w7 = P_L_given_Y**2 * P_notL_given_Y**1 * s**6 * q**4
    w8 = P_L_given_Y**3 *                  s**7 * q**4
    
    total = w1 + w2 + w3 + w4 + w5 + w6 + w7 + w8
    alpha = 1 / total
    pi = [alpha * w for w in [w1, w2, w3, w4, w5, w6, w7, w8]]
    
    # === BAR CHART ===
    fig = go.Figure(data=[go.Bar(
        x=[1,2,3,4,5,6,7,8],
        y=pi,
        marker_color="#3498db",
        text=[f"{p:.3f}" for p in pi],
        textposition="outside"
    )])
    fig.update_layout(
        title="Stationary Distribution π (State 1 = memorized, 8 = forgotten)",
        xaxis_title="Memory State",
        yaxis_title="Probability",
        yaxis=dict(range=[0,1]),
        template="simple_white"
    )
    
    return fig, f"P(Ī|Y) = {P_notL_given_Y:.3f}    |    P(Ȳ) = {P_notY:.3f}    |    q = {q:.3f}"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)