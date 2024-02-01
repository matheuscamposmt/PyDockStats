import streamlit as st
from pydockstats import calculate_curves
import plotly.graph_objects as go


# Functions to plot the curves
def plot_pc_curve(fig, program_name, curve_data):
    x, y = curve_data['x'], curve_data['y']
    auc = curve_data['bedroc']
    text_legend = f"{program_name}"

    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode='lines', 
            name=text_legend, 
            line=dict(width=3), showlegend=True,
            hovertemplate='Quantile: %{x}<br>Activity probability: %{y}<br>'
        )
    )

def plot_roc_curve(fig, program_name, curve_data):
    x, y = curve_data['x'], curve_data['y']
    auc = curve_data['auc']
    text_legend = f"{program_name} | AUC={auc:.2f}"

    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode='lines', 
            name=text_legend, 
            line=dict(width=3), showlegend=True,
            hovertemplate='FPR: %{x}<br>TPR: %{y}<br>'
        )
    )


class Curve:
    def __init__(self, name, title, xaxis_title, yaxis_title):
        self.name = name
        st.subheader(title)
        self.container = st.container()
        self.__fig = go.Figure(layout=dict(title=dict(text=title, font=dict(size=20)), xaxis_title=xaxis_title,
                                        yaxis_title=yaxis_title, legend=dict(orientation="v"), height=600, width=1000,
                                        font=dict(family='Montserrat', size=18), legend_title_text="Programs"))
        self.__fig.update_xaxes(range=[0, 1], constrain='domain', showgrid=True, showline=True, linewidth=1)
        self.__fig.update_yaxes(range=[0, 1], constrain='domain', showgrid=True, showline=True, linewidth=1)

    def add_plot(self, program_name):
        scores, activity = st.session_state.data[program_name]['scores'], st.session_state.data[program_name]['activity']
        data = calculate_curves(program_name, scores, activity)
        curve_data = data[0] if self.name == "PC" else data[1]
        plot_function = plot_pc_curve if self.name == "PC" else plot_roc_curve
        
        with self.container:
            plot_function(self.__fig, program_name, curve_data)

    def get_figure(self):
        return self.__fig

    def render(self):
        self.container.plotly_chart(self.__fig)

    def write_image(self, path):
        self.__fig.write_image(path)


class PredictivenessCurve(Curve):
    def __init__(self):
        super().__init__("PC", "Predictiveness Curve", "Quantile", "Activity probability")


class ReceiverOperatingCharacteristic(Curve):
    def __init__(self):
        super().__init__("ROC", "Receiver Operating Characteristic", "False Positive Rate", "True Positive Rate")

        


def generate_charts() -> (Curve, Curve):
    pc = PredictivenessCurve()
    roc = ReceiverOperatingCharacteristic()
    for program_tab in st.session_state['programs']:
        pc.add_plot(program_tab.get_program_name(),)
        roc.add_plot(program_tab.get_program_name())

    pc.render()
    roc.render()
    return pc, roc