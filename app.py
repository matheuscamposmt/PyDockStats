import streamlit as st
import app_utils as utils
from introduction import intro, helper
from tabs import input_programs, generate_tabs
from charts import generate_charts
import sys
import path

dir = path.Path(__file__).abspath()
sys.path.append(dir.parent.parent)

# Set page width
utils.set_max_width(70)
# Initialize session states
utils.initialize_session_states()

# introduction
intro()
helper()

# tabs
input_programs()
generate_tabs()

if len(st.session_state['programs']) > 0:
    if list(st.session_state['data'].keys()) == st.session_state['programs']:
        # generate the figures
        fig_pc, fig_roc = generate_charts()

        # download the figures and send to an input email
        email_expander = st.expander("Send to email")
        with email_expander:
            st.markdown("""
                        You can send the figures to an email by clicking on the send button below.
                        """)

            email = st.text_input("Enter your email")
            if st.button("Send"):
                if email:
                    figures = [fig_pc, fig_roc]
                    image_attachments = utils.save_plotly_figures_as_images(figures)
                    utils.send_email_with_attachments(
                        to_email=email,
                        subject="PyDockStats Figures",
                        message="Here are the performance metric figures generated by PyDockStats.",
                        attachments=image_attachments
                    )


                    st.success("Email sent successfully!")
                else:
                    st.error("Please enter a valid email address.")

