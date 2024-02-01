import streamlit as st

def intro():
    st.image('assets/logo.png', width=300)
    st.title("PyDockStats")
    st.subheader("A Python tool for Virtual Screening performance analysis")

    # Add description
    st.markdown("""
                PyDockStats is an easy and versatile Python tool that builds ROC (Receiver operating characteristic) and Predictiveness Curve curves.

                It creates a **logistic regression model** from the data and analyzes the relationship between the score of the molecule 
                and the activity to understand if the score has a effect on the activity and have the ability to separate the **True Positives** from the **False Positives**. 
                - **ROC curve** is a graphical plot that describes the performance of a binary classifier By mapping the relationship between the true positive rate and 
                the false positive rate, it quantifies the classifier's ability to distinguish between accurate positives and false alarms.
                - **PC (Predictiveness Curve)** is a graphical plot that measures the ability of a Virtual Screening program to separate 
                the data into true positives (true active) and false positives (decoys) and  (1) quantify and compare the predictive
                power of scoring functions above a given score quantile; (2) define a score threshold for prospective virtual
                screening, in order to select an optimal number of compounds to be tested experimentally in a drug discovery program.
                
                Therefore, the tool is useful when verifying Virtual Screening programs' performance and gaining more confidence when making inferences.""")
    
def helper():
    with st.expander("How to use"):
        st.markdown("""
                    With PyDockStats you can add as many programs as you want using the **"Add Program"** button below. The button will create a new expander with the name of the program.
                    
                    In each program expander you can:
                    1. Paste the scores of the ligands and decoys in the data editor.
                    2. Preview the data to ensure it is correct.
                    3. View the PC and ROC curves generated from the data.
                    4. Download the figures by clicking on the download button below the charts.
                    5. Send the figures to an email.
                    """)