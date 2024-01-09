import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt  # Import matplotlib
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pydockstats import calculate_curves
import numpy as np


def set_max_width(pct_width: int = 70):
    max_width_str = f"max-width: {pct_width}%;"
    st.markdown(
        f"""<style>.appview-container .main .block-container{{{max_width_str}}}</style>""",
        unsafe_allow_html=True,
    )

# Function to initialize session states
def initialize_session_states():
    if 'decoy_data' not in st.session_state:
        st.session_state.decoy_data = None
    if 'ligand_data' not in st.session_state:
        st.session_state.ligand_data = None
    if 'data' not in st.session_state:
        st.session_state.data = dict()

    if 'programs' not in st.session_state:
        st.session_state.programs = []


def get_matplotlib_ROC_plot():

    fig, ax = plt.subplots(figsize=(12, 7))
    for expander in st.session_state['programs']:
        program_name = expander.get_program_name()
        _, roc_data = calculate_curves(program_name, st.session_state['data'][program_name]['scores'], st.session_state['data'][program_name]['activity'])
        x,y = roc_data['x'], roc_data['y']
        auc = roc_data['auc']
        ax.plot(x, y, label=f"{program_name} | AUC={auc:.2f}")
    
    # Random line of the ROC curve
    random_x = np.linspace(0, 1, 100)
    random_y = random_x
    ax.plot(random_x, random_y, linestyle='--', color='gray', label='Random')
        

    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC")
    ax.legend()
    return fig

def get_matplotlib_PC_plot():
    fig, ax = plt.subplots(figsize=(12, 7))

    for expander in st.session_state['programs']:
        program_name = expander.get_program_name()
        print(st.session_state['data'][program_name])
        pc_data, _ = calculate_curves(program_name, st.session_state['data'][program_name]['scores'], st.session_state['data'][program_name]['activity'])
        x,y = pc_data['x'], pc_data['y']
        ax.plot(x, y, label="program_name")

    mean_value = st.session_state['data'][program_name]['scores'].mean()
    ax.axhline(mean_value, color='gray', linestyle='--', label=f"Mean = {mean_value:.2f}")
    
    ax.set_xlabel("Quantile")
    ax.set_ylabel("Activity probability")
    ax.set_title("PC")
    ax.legend()
    return fig

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

# Function to display data preview
def display_data_preview(df):
    st.subheader("Data Preview")
    st.dataframe(df)




# Function to send email with attachments
def send_email_with_attachments(to_email, subject, message, attachments):
    from_email = "matheuscamposmattos@id.uff.br"
    password = "jdehlcenifasfjmb"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    for attachment in attachments:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="test"')
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

# ----------------------------- #