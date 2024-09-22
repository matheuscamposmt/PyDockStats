import streamlit as st

def intro():
    st.image('./src/assets/logo.png', width=250)
    st.title("PyDockStats")
    st.subheader("A Python tool for Virtual Screening performance analysis")

def about():

    with st.container(border=True):

        # Add description
        st.markdown("""
                    PyDockStats is an easy and versatile Python tool that builds ROC (Receiver operating characteristic) and Predictiveness Curve curves.

                    It creates a **logistic regression model** from the data and analyzes the relationship between the score of the molecule 
                    and the activity to understand if the score has a effect on the activity and have the ability to separate the **True Positives** from the **False Positives**. Also, the tool
                    can be useful when deciding the cutoff value and the number of compounds to be tested experimentally in a drug discovery program. 

                    - **ROC curve** is a graphical plot that describes the performance of a binary classifier. By plotting the True Positive Rate (TPR) against the False Positive Rate (FPR) at various threshold settings, 
                    the ROC curve has the ability to visualize the trade-offs between the true positive rate and false positive rate as the discrimination threshold is varied. Also, the area under the ROC curve (AUC) is 
                    a measure of the ability of a scoring function to separate the data into true positives (true active) and false positives (decoys).

                    - Similarly **PC (Predictiveness Curve)** is a graphical plot that measures the ability of a Virtual Screening program to separate 
                    the data into true positives (true active) and false positives (decoys) and  (1) quantify and compare the predictive
                    power of scoring functions above a given score quantile; (2) define a score threshold for prospective virtual
                    screening, in order to select an optimal number of compounds to be tested experimentally in a drug discovery program.

                    - **Precision-Recall curve** is a graphical plot that describes the trade-off between the precision and the recall of a binary classifier.
                    The precision is the ratio of the True Positives to the sum of True Positives and False Positives, i.e the probability of a compound being active given that the model predicted it as active.
                    The recall is the ratio of the True Positives to the sum of True Positives and False Negatives, i.e the probability of a compound being predicted as active given that it is active.
                    The Precision-Recall curve is useful when the dataset is imbalanced, i.e the number of actives is much smaller than the number of decoys.
                    
                    Therefore, the tool is useful when verifying Virtual Screening programs performance and can be used to compare different programs.
                    
                    In summary, **PyDockStats** (PDS) is a user-friendly tool that support researchers in the field of drug discovery and development to get confidence and insights about the performance of their Virtual Screening programs.""")

    
def general_help():
    with st.expander("How to use"):
        st.markdown("""
                    With PyDockStats you can add as many programs as you want using the **➕ Add Program** button below. The button will create a new expander with the name of the program. 
                    In each program expander you can paste the scores of the ligands and decoys in the data editor, being able to add as many rows as you want and preview the data in a table.

                    You can also generate artificial scores for ligands and decoys using the **🧪 Generate fake data** button. This will create a new expander with the name **Artificial Scores**.
                    
                    - After adding the scores, you can click on the **✨ Generate** button to create the ROC and PC curves for each program.

                    - The tool will create a logistic regression model from the data and analyze the relationship between the score of the molecule and the activity to understand if the score has a effect on the activity and have the ability to separate the **True Positives** from the **False Positives**.

                    - The ROC and PC curves will be displayed in the same page and you can download the figures using the **📥 Download** button below each figure.

                    - Also, you can send the figures to your email on the bottom of the page.

                    - Finally, you can save your progress using the **💾 Save progress** button on the sidebar and then download the checkpoint (.pkl). Later, you can **📁 Upload the checkpoint file**, **📤 Load** it and continue your analysis from where you left off.
                    """)
        
def pc_interpretation_help():
    with st.expander("🤔 How to interpret the curve?"):
        
        st.markdown("""
                    The capacity of the models to highlight the score gaps between actives and decoys and transform those difference into probabilities is the core of PC.
                    The PC curve is a plot of the ascending ordered activity probabilities of the compounds in the dataset as a function of the fraction of the dataset that is considered.
                    Where the curve is steep, means that the model suddenly increased the probability of finding an active compound. The steeper the curve, the better the model is at separating actives from decoys.
                    """)


def roc_interpretation_help():
    with st.expander("🤔 How to interpret the curve?"):
        st.markdown("""
                    Each point is a different threshold for the logistic regression model to decide if a compound is active or not. For each point, the True Positive Rate (TPR) and the False Positive Rate (FPR) are calculated,
                    and the ROC curve is a plot of the TPR against the FPR. The ROC curve has the ability to visualize the trade-offs between the Sensitivity (TPR) and the Specificity (1 - FPR) as the discrimination threshold is varied. 
                    In other wordswe want to maximize Sensitivity and the Specificity at the same time, but in practice this is not totally possible, so the ROC curve is a way to find the best configuration that 
                    equilibrate both measures. Also, the **Area Under** the ROC **Curve** (AUC) is the overall measure of the ability of a scoring function to distinguish between true positives (true active) and false positives (decoys).
                    """)
        
def precision_recall_interpretation_help():
    with st.expander("🤔 How to interpret the curve?"):
        st.markdown("""
                    The Precision-Recall curve is a plot of the Precision against the Recall. The Precision is the ratio of the True Positives to the sum of True Positives and False Positives, i.e
                    the probability of a compound being active given that the model predicted it as active. Maximizing the precision means that the model is more selective in predicting actives.
                    The Recall is the ratio of the True Positives to the sum of True Positives and False Negatives, i.e the probability of a compound being predicted as active given that it is active.
                    Maximizing the recall means that the model is more sensitive in predicting actives. The Precision-Recall curve is useful when the dataset is imbalanced, i.e the number of actives is much smaller than the number of decoys.
                    """)