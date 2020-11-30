import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from django_plotly_dash import DjangoDash
from sympy import latex, sympify, integrate, Symbol
import math
from numpy import linspace
import dash_defer_js_import as dji


external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']

app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets, external_scripts=[
  'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML',
])

mathjax_script = dji.Import(src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/latest.js?config=TeX-AMS-MML_SVG")
refresh_plots = dji.Import("https://codepen.io/chrisvoncsefalvay/pen/ExPJjWP.js")

app.layout = html.Div([
    html.Div(["First function: ",
              dcc.Input(id='fn1', value='x**2', type='text')]),
    html.Br(),
    html.Div(["Second function: ",
              dcc.Input(id='fn2', value='x', type='text')]),
    html.Br(),
    html.Div(["Limits: ",
              dcc.Input(id='lower_limit', value='-1', type='text'),
              dcc.Input(id='upper_limit', value='1', type='text')]),
    html.Br(),
    html.H3("Area between curves:"),
    html.H3(id='my-output'),
    html.Div([dcc.Graph(id='graph')]),
    refresh_plots,
    mathjax_script

])


@app.callback(
    [Output(component_id='my-output', component_property='children'),
     Output('graph', 'figure')],
    [Input(component_id='fn1', component_property='value'),
     Input(component_id='fn2', component_property='value'),
     Input(component_id='lower_limit', component_property='value'),
     Input(component_id='upper_limit', component_property='value')]
)
def update_output_div(fn1, fn2, lower_limit, upper_limit):
    def to_float(s):
        constants = {"pi": 3.14159, "e": 2.71928, "-pi": -3.14159, "-e": -2.71928,
                     "inf": math.inf, "-inf": -math.inf}
        if s in constants:
            return constants[s]
        else:
            return float(s)

    def f(x):
        return eval(fn1)

    def g(x):
        return eval(fn2)

    x = Symbol('x')
    l = to_float(lower_limit)
    u = to_float(upper_limit)

    output = integrate(f(x) - g(x), (x, l, u))

    x = linspace(l, u, 30)
    y1 = [f(x) for x in x]
    y2 = [g(x) for x in x]
    t = "r'$\\int_{" + lower_limit + "}^{" + upper_limit + "}" + latex(sympify(fn1)) + " - " + latex(
        sympify(fn2)) + "$"

    figure = px.line(x=x, y=[y1, y2], title=t)

    out = '{}'.format(output)



    return out, figure
