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


class PredictivenessCurve:
    def __init__(self):
        self.name = "PC"
        st.subheader("Predictiveness Curve")
        self.__pc_container = st.container()
        self.__fig = go.Figure(layout=dict(title=dict(text="PC", font=dict(size=20)), xaxis_title="Quantile", yaxis_title="Activity probability",
                                        legend=dict(orientation="v"), height=600, width=1000, font=dict(family='Montserrat', size=16), legend_title_text="Programs"))
        self.__fig.update_xaxes(range=[0, 1], constrain='domain', showgrid=False)
        self.__fig.update_yaxes(range=[0, 1], constrain='domain', showgrid=False)
    
    def add_plot(self, program_name):
        scores, activity = st.session_state.data[program_name]['scores'], st.session_state.data[program_name]['activity']
        pc_data = calculate_curves(program_name, scores, activity)[0]
        with self.__pc_container:
            plot_pc_curve(self.__fig, program_name, pc_data)
    
    def render(self):
        self.__pc_container.plotly_chart(self.__fig)

    def write_image(self, path):
        self.__fig.write_image(path)
    
class ReceiverOperatingCharacteristic:
    def __init__(self):
        self.name = "ROC"
        st.subheader("Receiver Operating Characteristic")
        self.__roc_container = st.container()
        self.__fig = go.Figure(layout=dict(title=dict(text="ROC", font=dict(size=20)), xaxis_title="False Positive Rate", 
                                        yaxis_title="True Positive Rate", legend=dict(orientation="v"), height=600, width=900,
                                        font=dict(family='Montserrat', size=16), legend_title_text="Programs"))
        self.__fig.update_xaxes(range=[0, 1], constrain='domain', showgrid=False)
        self.__fig.update_yaxes(range=[0, 1], constrain='domain', showgrid=False)

    
    def add_plot(self, program_name):
        scores, activity = st.session_state.data[program_name]['scores'], st.session_state.data[program_name]['activity']
        roc_data = calculate_curves(program_name, scores, activity)[1]
        with self.__roc_container:
            plot_roc_curve(self.__fig, program_name, roc_data)
        
    def render(self):
        self.__roc_container.plotly_chart(self.__fig)

    def write_image(self, path):
        self.__fig.write_image(path)


        

def generate_charts():
    pc = PredictivenessCurve()
    roc = ReceiverOperatingCharacteristic()
    for program_tab in st.session_state['programs']:
        pc.add_plot(program_tab.get_program_name())
        roc.add_plot(program_tab.get_program_name())

    pc.render()
    roc.render()
    return pc, roc