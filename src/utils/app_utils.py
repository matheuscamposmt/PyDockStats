import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt  # Import matplotlib
from email import encoders
from model.pydockstats import calculate_curves
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# function to inject the google search console meta tag
def activate_google_analytics():
    with open("google_analytics.html", "r") as f:
        html_code = f.read()
        st.markdown(html_code, unsafe_allow_html=True)

    print("Google Analytics activated")
    

def set_max_width(pct_width: int = 70):
    max_width_str = f"max-width: {pct_width}%;"
    st.markdown(
        f"""<style>.appview-container .main .block-container{{{max_width_str}}}</style>""",
        unsafe_allow_html=True,
    )

# Function to initialize session states
def initialize_session_states():
    if 'programs' not in st.session_state:
        st.session_state.programs = []

    if 'paths' not in st.session_state:
        st.session_state.paths = dict()



def get_plt_from_plotly(plotly_fig: go.Figure) -> plt.Figure:
    # create a matplotlib figure like the plotly figure from a go.Figure object
    plt.style.use(['science', 'no-latex'])

    plt_fig, ax = plt.subplots(figsize=(10, 7))

    def convert_line_dash(dash):
        if dash == 'dash':
            return '--'
        elif dash == 'dot':
            return ':'
        else:
            return '-'
        
    def format_trace_label(label: str):
        return label.replace('<br>', '').replace('<b>', '').replace('</b>', '')
        
    plotly_fig.for_each_trace(lambda trace: ax.plot(trace.x, trace.y, label=format_trace_label(trace.name), linewidth=trace.line.width*0.8, 
                                                    linestyle=convert_line_dash(trace.line.dash), color=trace.line.color))

    ax.set_xlabel(plotly_fig.layout.xaxis.title.text, fontsize=14)
    ax.set_ylabel(plotly_fig.layout.yaxis.title.text, fontsize=14)
    ax.set_title(plotly_fig.layout.title.text, fontsize=17)

    plt.grid(True, alpha=0.2, linewidth=0.4, color='black')

    x_range = plotly_fig.layout.xaxis.range
    y_range = plotly_fig.layout.yaxis.range
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)
    #ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
    ax.legend(loc='best', fontsize=11, frameon=True)

    return plt_fig

# Function to upload ligands and decoys files
def upload_files(program_name):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Ligands")
        ligands_file = st.file_uploader("Choose a .csv or .lst file for the ligands", 
                                        type=['csv', 'lst', 'xlsx'], key=f"{program_name}_ligands")
    with col2:
        st.markdown("#### Decoys")
        decoys_file = st.file_uploader("Choose a .csv or .lst file for the decoys", 
                                    type=['csv', 'lst', 'xlsx'], key=f"{program_name}_decoys")
    return ligands_file, decoys_file

