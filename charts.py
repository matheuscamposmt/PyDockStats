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
        self.__fig = go.Figure(layout=dict(title=dict(text=title, font=dict(size=25)), xaxis_title=xaxis_title,
                        yaxis_title=yaxis_title, legend=dict(orientation="v"),autosize=True, height=600,
                        font=dict(family='Montsserrat'), legend_title_text="Programs",
                        spikedistance=-1))
        self.__fig.update_xaxes(range=[0, 1], constrain='domain', showgrid=True, showline=True, linewidth=1,
                                showspikes=True, spikemode='across', spikesnap='cursor')
        self.__fig.update_yaxes(range=[0, 1], constrain='domain', showgrid=True, showline=True, linewidth=1)
        self.__fig.update_layout(margin=dict(l=60, r=60, b=0, t=100), plot_bgcolor='white')
        # increase the font sizes, except for the title
        self.__fig.update_layout(xaxis_title_font_size=20, yaxis_title_font_size=20, legend_font_size=15)

        self._color_palette = ['#0C5DA5', '#00B945', '#FF9500', '#FF2C00', '#845B97', '#474747', '#9e9e9e']
        self.curves: Dict[str, go.Scatter] = dict()
        
    def add_trace(self, curve: go.Scatter) -> None:
        self.curves[curve.name] = curve
        self.__fig.add_trace(curve)

    def get_figure(self) -> go.Figure:
        return self.__fig

    def render(self) -> None:
        st.plotly_chart(self.__fig, use_container_width=True, config=dict(displayModeBar=True, displaylogo=False))

    def write_image(self, path) -> None:
        self.__fig.write_image(path)


class Predictiveness(Chart):
    def __init__(self):
        super().__init__("PC", "Predictiveness Curve", "Quantile", "Activity probability")

        
    def add_plot(self, program: Program):
        x, y = program.quantiles, program.probabilities
        enrichment_factors = program.enrichment_factors

        legend_title = f"{program.name}"
        hover = 'Quantile: %{x:.2f}<br>Activity probability: %{y:.2f}<br>Enrichment Factor: %{customdata:.3f}'

        curve = go.Scatter(x=x, y=y, mode='lines', name=legend_title, line=dict(width=3, color=self._color_palette[len(self.curves)]),
                            showlegend=True, hovertemplate=hover,
                            customdata=enrichment_factors,
                            legendgroup=program.name, fill=None)
        self.curves[program.name] = curve
        self.add_trace(curve)

    def add_prevalence_line(self, programs: List[Program]):
        prevalence = sum([program.prevalence for program in programs]) / len(programs)
        prevalence_line = go.Scatter(x=[0, 1], y=[prevalence, prevalence], mode='lines', name='Prevalence',
                                     line=dict(width=1, color='gray', dash='dash'), showlegend=True, hoverinfo='skip')
        self.add_trace(prevalence_line)


class ReceiverOperatingCharacteristic(Chart):
    def __init__(self):
        super().__init__("ROC", "Receiver Operating Characteristic", "False Positive Rate", "True Positive Rate")        
        # add a diagonal line
        random_line = go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Random', line=dict(width=1, color='red', dash='dash'),
                                 showlegend=True, hoverinfo='skip')
        self.add_trace(random_line)
       

    def add_plot(self, program: Program):
        x, y = program.fpr, program.tpr
        thresholds=program.thresholds 
        
        legend_title = f"{program.name}: <br><b>AUC={program.auc:.3f}</b>"
        hover = 'False Positive Rate: %{x}<br>True Positive Rate: %{y}<br>' + f'AUC={str(program.auc)}' + '<br>Threshold=%{customdata:.3f}'

        curve = go.Scatter(x=x, y=y, mode='lines', name=legend_title, line=dict(width=3, color=self._color_palette[len(self.curves)]),
                            showlegend=True, hovertemplate=hover,
                            customdata=program.thresholds,
                            legendgroup=program.name)
        

        self.add_trace(curve)