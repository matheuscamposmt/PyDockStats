import streamlit as st
from pydockstats import calculate_curves
import plotly.graph_objects as go
from program import Program
from typing import List, Dict


# Functions to plot the curve
def plot_curve(chart, program_name, x, y, **kwargs):
    chart.add_trace(
        go.Scatter(
            x=x, y=y, mode='lines',
            name=kwargs['legend'],
            line=dict(width=3), showlegend=True,
            hovertemplate = kwargs['hovertemplate']


        )
    )



class Chart:
    def __init__(self, name, title, xaxis_title, yaxis_title):
        self.name = name
        self.xaxis_title = xaxis_title
        self.yaxis_title = yaxis_title
        self.__fig = go.Figure(layout=dict(title=dict(text=title, font=dict(size=20)), xaxis_title=xaxis_title,
                                        yaxis_title=yaxis_title, legend=dict(orientation="v"),autosize=True, height=600,
                                        font=dict(family='Montserrat', size=20), legend_title_text="Programs"))
        self.__fig.update_xaxes(range=[0, 1], constrain='domain', showgrid=True, showline=True, linewidth=1)
        self.__fig.update_yaxes(range=[0, 1], constrain='domain', showgrid=True, showline=True, linewidth=1)

    def add_trace(self, curve: go.Scatter) -> None:
        self.__fig.add_trace(curve)

    def get_figure(self) -> go.Figure:
        return self.__fig

    def render(self) -> None:
        st.plotly_chart(self.__fig, use_container_width=True, config=dict(displayModeBar=True, displaylogo=False))

    def write_image(self, path) -> None:
        self.__fig.write_image(path)


class Curve(go.Scatter):
    def __init__(self, x, y, program: Program, **kwargs):
        super().__init__(x=x, y=y, mode='lines', name=program.name, line=dict(width=3), 
                         showlegend=True, hovertemplate=kwargs['hovertemplate'],
                         legend=kwargs['legend'])
        self.__program = program


class Predictiveness(Chart):
    def __init__(self):
        super().__init__("PC", "Predictiveness Curve", "Quantile", "Activity probability")
        self.__curves: Dict[str, Curve] = dict()
        
    def add_plot(self, program: Program):
        x, y = program.quantiles, program.probabilities
        curve = Curve(x, y, program, 
                      hovertemplate='Quantile: %{x}<br>Activity probability: %{y}<br>',
                      legend=None)
        self.__curves[program.name] = curve
        self.add_trace(curve)


class ReceiverOperatingCharacteristic(Chart):
    def __init__(self):
        super().__init__("ROC", "Receiver Operating Characteristic", "False Positive Rate", "True Positive Rate")   

    def add_plot(self, program: Program):
        x, y = program.fpr, program.tpr
        curve = Curve(x, y, program,
                      hovertemplate='False Positive Rate: %{x}<br>True Positive Rate: %{y}<br>',
                      legend=None)
        self.add_trace(curve)