import streamlit as st
from pydockstats import calculate_curves
import plotly.graph_objects as go
from program import Program
from typing import List, Dict


class Chart:
    def __init__(self, name, title, xaxis_title, yaxis_title):
        self.name = name
        self.xaxis_title = xaxis_title
        self.yaxis_title = yaxis_title
        self.__fig = go.Figure(layout=dict(title=dict(text=title, font=dict(size=20)), xaxis_title=xaxis_title,
                        yaxis_title=yaxis_title, legend=dict(orientation="v"),autosize=True, height=600,
                        font=dict(family='Montserrat', size=20), legend_title_text="Programs",
                        spikedistance=-1))
        self.__fig.update_xaxes(range=[0, 1], constrain='domain', showgrid=True, showline=True, linewidth=1,
                                showspikes=True, spikemode='across', spikesnap='cursor')
        self.__fig.update_yaxes(range=[0, 1], constrain='domain', showgrid=True, showline=True, linewidth=1)
        self._color_palette = ['#0C5DA5', '#00B945', '#FF9500', '#FF2C00', '#845B97', '#474747', '#9e9e9e']
        self.curves: Dict[str, Curve] = dict()
        
    def add_trace(self, curve: go.Scatter) -> None:
        self.curves[curve.name] = curve
        self.__fig.add_trace(curve)

    def get_figure(self) -> go.Figure:
        return self.__fig

    def render(self) -> None:
        st.plotly_chart(self.__fig, use_container_width=True, config=dict(displayModeBar=True, displaylogo=False))

    def write_image(self, path) -> None:
        self.__fig.write_image(path)


class Curve(go.Scatter):
    def __init__(self, x, y, program: Program, **kwargs):
        super().__init__(x=x, y=y, mode='lines', name=program.name, line=dict(width=3, color=kwargs['color']), 
                         showlegend=True, hovertemplate=kwargs['hovertemplate'],
                         legend=kwargs['legend'])


class Predictiveness(Chart):
    def __init__(self):
        super().__init__("PC", "Predictiveness Curve", "Quantile", "Activity probability")

        
    def add_plot(self, program: Program):
        x, y = program.quantiles, program.probabilities
        curve = Curve(x, y, program, 
                      hovertemplate='Quantile: %{x}<br>Activity probability: %{y}<br>',
                      legend=None, color=self._color_palette[len(self.curves)])
        self.curves[program.name] = curve
        self.add_trace(curve)


class ReceiverOperatingCharacteristic(Chart):
    def __init__(self):
        super().__init__("ROC", "Receiver Operating Characteristic", "False Positive Rate", "True Positive Rate")   

    def add_plot(self, program: Program):
        x, y = program.fpr, program.tpr
        curve = Curve(x, y, program,
                      hovertemplate='False Positive Rate: %{x}<br>True Positive Rate: %{y}<br>',
                      legend=None, color=self._color_palette[len(self.curves)])
        self.add_trace(curve)