import pickle
# app imports ----------------
import streamlit as st
import utils.app_utils as utils
import info as info
from components.expander import ProgramsExpanders
from components.charts import Predictiveness, ReceiverOperatingCharacteristic, PrecisionRecall
from utils.saving import EmailSender, FigureDownloader
from utils.putils import generate_artificial_scores

# Set the page configuration
st.set_page_config(
    page_title="Home • PyDockStats",
    page_icon="🏠",
    layout="wide"
)

# Set the maximum width for the app
utils.set_max_width(90)

# Initialize session states
utils.initialize_session_states()

# Display introduction and general help information
info.intro()
info.general_help()

# Initialize the expanders for programs
programs_expanders = ProgramsExpanders()

# Sidebar for checkpoints
st.sidebar.header("📌Checkpoints")
save_cp_container = st.sidebar.container()
upload_cp_container = st.sidebar.container()

# Upload checkpoint section
with upload_cp_container:
    input_checkpoint = st.file_uploader("📁 Upload a checkpoint file", type="pkl", key="input_checkpoint", 
                                        help="Upload a checkpoint file to continue from where you left off")
    load_button = st.button("📤 Load", key="load", type='secondary', help="Load a checkpoint file", disabled=not input_checkpoint,
                            use_container_width=True)
    
    if input_checkpoint and load_button:
        # Load the checkpoint file
        import_dict = pickle.loads(input_checkpoint.read())

        # Update the expanders with the loaded data
        programs_expanders.from_data_dict(import_dict)

        # Reset the cached images paths
        st.session_state['paths'] = dict()

        # Generate the expanders
        programs_expanders.generate()

        st.success("✔️ Checkpoint loaded successfully.")

# Save checkpoint section
with save_cp_container:
    save_col, download_col = st.columns(2)
    save_button = save_col.button("💾 Save progress", key="save", 
                                  type='secondary', help="Save the current state of the app",
                                  disabled=not programs_expanders.all_data_generated())

# Programs section
st.subheader("Programs")
program_name_container = st.container()
with program_name_container:
    program_name = st.text_input("Enter the name of the program (optional)", placeholder="Autodock Vina",
                                 max_chars=30, value="", key='program_name')
    
    add_program_col, generate_data_col = st.columns([1, 7], gap='small')
    
    with add_program_col:
        add_program = st.button("➕ Add program", help="Add a new program expander",
                                type='secondary', disabled=len(st.session_state['programs']) > 15)
    
    with generate_data_col:
        generate_data = st.button("🧪 Generate fake data", help="Generate artificial data for testing purposes", 
                                  key="generate_data")
    if generate_data:
        program_id = st.session_state['programs'][-1].id + 1 if st.session_state['programs'] else 1
        data= generate_artificial_scores(200)
        programs_expanders.add_program_expander(f"Artificial Data {program_id}", expand=False)
        programs_expanders.programs[-1].set_data(data['ligands'], data['decoys'])

    if add_program:
        program_id = st.session_state['programs'][-1].id + 1 if st.session_state['programs'] else 1
        name = program_name.strip() if program_name else f"Program {program_id}"
        programs_expanders.add_program_expander(name)

# Render the expanders
programs_expanders.render()

# Generate button
if len(st.session_state['programs']) > 0:
    generate_button = st.button("✨ Generate", key="generate",
                                use_container_width=True, type='primary',
                                help="Generate the performance metrics figures",
                                disabled=not programs_expanders.all_data_inputted())
                    
    if generate_button:
        st.session_state['paths'] = dict()
        with st.spinner("Generating data..."):
            programs_expanders.generate()
        st.rerun()

# If all data is generated, display the figures and download options
if programs_expanders.all_data_generated():
    downloader = FigureDownloader("figures", engine='matplotlib')

    with st.spinner("Generating figures..."):
        pc = Predictiveness()
        roc = ReceiverOperatingCharacteristic()
        precision_recall = PrecisionRecall()

        pc.add_prevalence_line(programs_expanders.programs)
        for program in programs_expanders.programs:
            pc.add_plot(program)
            roc.add_plot(program)
            precision_recall.add_plot(program)
        
        with st.container() as pc_container:
            pc.render()

            _, pc_download_col, _ = st.columns([1, 2, 1])

            st.write("")

            download_btn = pc_download_col.download_button(
                label="📥 Download chart",
                data=downloader.read_image(downloader.download(pc)),
                file_name="pc.png",
                mime="image/png",
                use_container_width=True,
                key="pc_download"
            )
            info.pc_interpretation_help()

        # Receiver Operating Characteristic (ROC)
        with st.container() as roc_container:
            roc.render()
            _, roc_download_col, _ = st.columns([1, 2, 1])
            st.write("")
            download_btn = roc_download_col.download_button(
                label="📥 Download chart",
                data=downloader.read_image(downloader.download(roc)),
                file_name="roc.png",
                mime="image/png",
                use_container_width=True,
                key="roc_download"
            )
            info.roc_interpretation_help()
            
            with st.expander("### BEDROC Metric"):
                st.markdown(
                    """
                    ### BEDROC (Boltzmann-Enhanced Discrimination of ROC) Metric
                    BEDROC is a metric that evaluates the enrichment of the top-ranked compounds in a virtual screening experiment.
                    It is a variation of the ROC curve that penalizes early false positives more than the ROC curve.
                    
                    The metric below shows the BEDROC value for each program, with the delta value compared to the previous program.
                    """
                )

            # BEDROC metric
            num_programs = len(programs_expanders.programs)
            num_cols = 3
            num_rows = (num_programs + num_cols - 1) // num_cols  # Calculate the number of rows needed

            for row in range(num_rows):
                cols = st.columns(num_cols)
                for col_idx in range(num_cols):
                    program_idx = row * num_cols + col_idx
                    if program_idx < num_programs:
                        program = programs_expanders.programs[program_idx]
                        with cols[col_idx]:
                            if program_idx > 0:
                                previous_bedroc = programs_expanders.programs[program_idx - 1].bedroc
                                delta = program.bedroc - previous_bedroc
                            else:
                                delta = 0.0
                            st.metric(label=f"{program.name} BEDROC", value=round(program.bedroc, 3),
                                      delta=round(delta, 3), delta_color='normal')



        # Precision-Recall Curve
        with st.container() as precision_recall_container:
            precision_recall.render()
            _, pr_download_col, _ = st.columns([1, 2, 1])
            st.write("")
            download_btn = pr_download_col.download_button(
                label="📥 Download chart",
                data=downloader.read_image(downloader.download(precision_recall)),
                file_name="precision_recall.png",
                mime="image/png",
                use_container_width=True,
                key="pr_download"
            )
            info.precision_recall_interpretation_help()

    # Save checkpoint
    with save_cp_container:
        if save_button:
            with open("checkpoint.pkl", "wb") as f:
                pickle.dump(programs_expanders.to_dict(), f)
            st.success("✔️ Checkpoint saved successfully.")
            download_button = download_col.download_button(
                label="📥 Download",
                data=open("checkpoint.pkl", "rb"),
                file_name="checkpoint.pkl",
                mime="application/octet-stream",
                key="download_checkpoint",
                use_container_width=True
            )

    st.divider()

    # Send figures to email
    email_expander = st.expander("📪 Send to email")
    with email_expander:
        email = st.text_input("Enter your email")
        send_button = st.button("📨 Send", key="send", type='primary', help="Send the figures to the email")
        if send_button:
            if email:
                # Loading bar
                progress_bar = st.progress(0)
                paths = [downloader.download(pc), downloader.download(roc), downloader.download(precision_recall)]
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
                st.error("Please enter an email address.")

