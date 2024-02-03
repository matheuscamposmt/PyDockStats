import streamlit as st
import app_utils as utils
import introduction as intro
from expander import ProgramsExpander
from program import Program
from charts import Chart, Predictiveness, ReceiverOperatingCharacteristic
import sys
import path
from saving import EmailSender, FigureDownloader
import pickle

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
intro.intro()
intro.general_help()
st.divider()

# programs expander
programs_expander = ProgramsExpander()

# checkpoints container
save_cp_container = st.sidebar.container(border=False)
upload_cp_container = st.sidebar.container()
with save_cp_container:
        save_col, download_col = st.columns(2)
        save_button = save_col.button("💾 Save progress", key="save", 
                                        type='secondary', help="Save the current state of the app",
                                        disabled= not programs_expander.all_data_generated())


with upload_cp_container:

    st.subheader("📌Checkpoints")
    input_checkpoint = st.file_uploader("Upload a checkpoint file ", type="pkl", key="input_checkpoint", 
                                        help="Upload a checkpoint file to continue from where you left off")
    load_button = st.button("📤 Load", key="load", type='secondary', help="Load a checkpoint file", disabled= not input_checkpoint,
                            use_container_width=True)
    # read the checkpoint file
    if input_checkpoint and load_button:
        programs_expander = pickle.loads(input_checkpoint.read())
        st.success("Checkpoint loaded successfully.")
        st.session_state['programs'] = programs_expander.expanders
                
    

st.subheader("Programs")
# program name input
program_name_container = st.container()
with program_name_container:
    program_name = st.text_input("Enter the name of the program (optional)", placeholder="Autodock Vina",
                                    max_chars=30, value="", key='program_name')
    
    add_program = st.button("➕ Add program", help="Add a new program expander",
                            type='secondary', disabled=len(st.session_state['programs']) > 15)
    
    if add_program and program_name not in st.session_state['programs']:
        program = Program(program_name.strip() if program_name else f"Program {len(st.session_state.programs) + 1}")
        programs_expander.add_program(program)


programs_expander.render()

# generate button
if len(st.session_state['programs']) > 0:
    generate_button = st.button("✨ Generate", key="generate",
                                            use_container_width=True, type='primary',
                                            help="Generate the performance metrics figures",
                                            disabled = not programs_expander.all_data_inputted())
                    
    if generate_button:
        st.session_state['paths'] = dict()
        with st.spinner("Generating data..."):
            programs_expander.generate()
        st.rerun()


if programs_expander.all_data_generated():
    downloader = FigureDownloader("figures", engine='matplotlib')

    with st.spinner("Generating figures..."):
        pc = Predictiveness()
        roc = ReceiverOperatingCharacteristic()

        
        for expander in programs_expander.expanders:
            program = expander.program
            pc.add_plot(program)
            roc.add_plot(program)

        with st.container() as pc_container:
            st.subheader("Predictiveness Curve (PC)")
            pc.render()

            _, pc_download_col, _ = st.columns([1, 2, 1])

            st.write("")

            download_btn = pc_download_col.download_button(
                label="Download",
                data=downloader.read_image(downloader.download(pc)),
                file_name="pc.png",
                mime="image/png",
                use_container_width=True,
                key="pc_download"
            )
            intro.pc_interpretation_help()


        with st.container() as roc_container:
            st.subheader("Receiver Operating Characteristic (ROC)")
            roc.render()
            _, roc_download_col, _ = st.columns([1, 2, 1])

            st.write("")
            download_btn = roc_download_col.download_button(
                label="Download",
                data=downloader.read_image(downloader.download(roc)),
                file_name="roc.png",
                mime="image/png",
                use_container_width=True,
                key="roc_download"
            )
            intro.roc_interpretation_help()


    with save_cp_container:

        if save_button:
            print(1)
            with open("checkpoint.pkl", "wb") as f:
                pickle.dump(programs_expander, f)
            st.success("Checkpoint saved successfully.")

            download_button = download_col.download_button(
                label="📥 Download",
                data=open("checkpoint.pkl", "rb"),
                file_name="checkpoint.pkl",
                mime="application/octet-stream",
                key="download_checkpoint",
                use_container_width=True
            )



    st.divider()


    # download the figures and send to an input email
    email_expander = st.expander("📪 Send to email")
    with email_expander:
        
        email = st.text_input("Enter your email")
        send_button = st.button("📨 Send", key="send", type='primary', help="Send the figures to the email")
        if send_button:
            if email:
                # loading bar
                progress_bar = st.progress(0)
                paths = [downloader.download(pc), downloader.download(roc)]
                progress_bar.progress(0.3)
                sender = EmailSender("smtp.gmail.com", 587)
                progress_bar.progress(0.7)
                result = sender.send_email_with_images(
                    email, "PyDockStats figures", paths
                )
                progress_bar.progress(1)
                if result['status'] == "success":
                    st.success(result['message'])
                    progress_bar.empty()

                else:
                    st.error(f"Email not sent. {result['message']}")
            else:
                st.error("Please enter a email address.")


