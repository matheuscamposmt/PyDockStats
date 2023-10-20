import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt  # Import matplotlib
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pydockstats import generate_plots

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

# Function to plot curves
def plot_curve(fig, program_name, curve_data, curve_name):
    x, y = curve_data['x'], curve_data['y']
    auc = curve_data['auc']
    text_legend = f"{program_name} | AUC={auc:.2f}" if curve_name == "ROC" else f"{program_name}"

    hover_template = 'FPR: %{x}<br>TPR: %{y}<br>' if curve_name == "ROC" else 'Quantile: %{x}<br>Activity probability: %{y}<br>'
    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode='lines', 
            name=text_legend, 
            line=dict(width=3), showlegend=True,
            hovertemplate=hover_template
        )
    )
    


# Function to save Plotly figures as images
def save_plotly_figures_as_images(figures):
    images = []
    for fig in figures:
        img_stream = BytesIO()
        plt.savefig(img_stream, format='png', bbox_inches='tight')
        img_stream.seek(0)
        images.append(img_stream)
        plt.close()
    return images

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