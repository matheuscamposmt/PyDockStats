import streamlit as st
import app_utils as utils
from introduction import intro, helper
from expander import ProgramExpanders
from program import Program
from charts import generate_charts
import sys
import path
from saving import EmailSender, FigureDownloader

st.set_page_config(
    page_title="PyDockStats",
    page_icon="assets/logo.png",
    layout="wide"
)

DIR = path.Path(__file__).abspath()
sys.path.append(DIR.parent.parent)

# Set page width
utils.set_max_width(70)
# Initialize session states
utils.initialize_session_states()

# introduction
intro()
helper()
# tabs
program_expanders = ProgramExpanders()

program_name_container = st.container()
with program_name_container:
    program_name = st.text_input("Enter the name of the program (optional)", placeholder="Autodock Vina",
                                    max_chars=30, value="", key='program_name')
    add_program = st.button("Add program", help="Add a new program tab",
                            type='secondary', disabled=len(st.session_state['programs']) > 15)
    
    if add_program and program_name not in st.session_state['programs']:
        program = Program(program_name.strip() if program_name else f"Program {len(st.session_state.programs) + 1}")
        program_expanders.add_program(program)

st.subheader("Programs")
program_expanders.render()
if program_expanders.data_inputted:

    generate_button = st.button("Generate", key="generate",
                                            use_container_width=True, type='primary',
                                            help="Generate the performance metrics figures")
                
    if generate_button:
        program_expanders.generate()

if len(st.session_state['programs']) > 0:
    if len(st.session_state['data'].keys()) == len(st.session_state['programs']):
        # generate the figures
        fig_pc, fig_roc = generate_charts()


        # download the figures and send to an input email
        email_expander = st.expander("Send to email")
        with email_expander:
            st.markdown("""
                        You can send the figures to an email by clicking on the send button below.
                        """)
            
            email = st.text_input("Enter your email")
            send_button = st.button("Send", key="send", type='primary', help="Send the figures to the email")
            if send_button:
                if email:
                    # loading bar
                    progress_bar = st.progress(0)
                    downloader = FigureDownloader("figures", engine='matplotlib')
                    progress_bar.progress(0.2)
                    paths = downloader.download([fig_pc, fig_roc])
                    progress_bar.progress(0.5)
                    sender = EmailSender("smtp.gmail.com", 587)
                    progress_bar.progress(0.8)
                    sender.send_email_with_images(
                        email, "PyDockStats figures", paths
                    )
                    progress_bar.progress(1)

                    st.success("Email sent successfully!")
                else:
                    st.error("Please enter a valid email address.")


