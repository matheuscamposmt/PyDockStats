import streamlit as st
from model.pydockstats import calculate_curves
import plotly.graph_objects as go
from components.program import Program
from typing import List, Dict

HEX_COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
    "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5",
    "#393b79", "#637939", "#8c6d31", "#843c39", "#7b4173",
    "#5254a3", "##793943", "#000000", "#bd9e39", "#ff00ff"
]


class Chart:
    def __init__(self, name, title, xaxis_title, yaxis_title, show_xspikes=False):
        self.programs: List[Program] = []
        self.curves: List[go.Scatter] = []
        self.name = name
        self.xaxis_title = xaxis_title
        self.yaxis_title = yaxis_title
        self.__fig = go.Figure(layout=dict(title=dict(text=title, font=dict(size=25)), xaxis_title=xaxis_title,
                        yaxis_title=yaxis_title, legend=dict(orientation="v"),autosize=True, height=600,
                        font=dict(family='Montsserrat'), legend_title_text="Programs",
                        spikedistance=-1))
        
        xspikes_params = {}
        if show_xspikes:
            xspikes_params = dict(showspikes=True, spikemode='across', spikesnap='cursor')

        self.__fig.update_xaxes(range=[0, 1], constrain='domain', showgrid=True, showline=True, linewidth=1,
                                **xspikes_params)
        
        self.__fig.update_yaxes(range=[0, 1], constrain='domain', showgrid=True, showline=True, linewidth=1)
        self.__fig.update_layout(margin=dict(l=60, r=60, b=0, t=100), plot_bgcolor='white')
        # increase the font sizes, except for the title
        self.__fig.update_layout(xaxis_title_font_size=20, yaxis_title_font_size=20, legend_font_size=15)

        self._color_palette = HEX_COLORS
        
    def add_trace(self, curve: go.Scatter) -> None:
        self.__fig.add_trace(curve)

    def add_program(self, program: Program) -> None:
        self.programs.append(program)

    def get_figure(self) -> go.Figure:
        return self.__fig

    def render(self) -> None:
        st.plotly_chart(self.__fig, use_container_width=True, config=dict(displayModeBar=True, displaylogo=False))

    def write_image(self, path) -> None:
        self.__fig.write_image(path)


class Predictiveness(Chart):
    def __init__(self):
        super().__init__("PC", "Predictiveness Curve", "Quantile", "Activity probability", show_xspikes=True)

    # TODO
    def on_click_quantile(self, quantile: float):
        st.markdown("You clicked on the quantile: " + str(quantile))
        
        for program in self.programs:
            st.metric(label=f"({program.name})", value=program.enrichment_factors[program.quantiles.index(quantile)], delta=0.01, delta_color='normal')

        
    def add_plot(self, program: Program):
        x, y = program.quantiles, program.probabilities

        legend_title = f"{program.name}"
        hover = 'Quantile: %{x:.2f}<br>Activity probability: %{y:.2f}<br>Enrichment Factor: %{customdata:.3f}'

        curve = go.Scatter(x=x, y=y, mode='lines', name=legend_title, line=dict(width=3, color=self._color_palette[len(self.curves)]),
                            showlegend=True, hovertemplate=hover,
                            customdata=program.enrichment_factors,
                            legendgroup=program.name)

        self.curves.append(curve)
        self.add_trace(curve)

        self.add_program(program)


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
        
        legend_title = f"{program.name}: <br><b>AUC={program.auc:.3f}</b>"
        hover = 'False Positive Rate: %{x:.3f}<br>True Positive Rate: %{y:.3f}<br>Threshold=%{customdata:.3f}'

        curve = go.Scatter(x=x, y=y, mode='lines', name=legend_title, line=dict(width=3, color=self._color_palette[len(self.curves)]),
                            showlegend=True, hovertemplate=hover,
                            customdata=program.thresholds,
                            legendgroup=program.name)
        
        self.curves.append(curve)
        self.add_trace(curve)

        self.add_program(program)