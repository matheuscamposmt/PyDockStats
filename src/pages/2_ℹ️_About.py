import streamlit as st
import info as info
import utils.app_utils as utils


st.set_page_config(
    page_title="About • PyDockStats",
    page_icon="ℹ️",
    layout="wide"

)

utils.set_max_width(90)

info.intro()
info.about()
