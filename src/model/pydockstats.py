import pandas as pd
import numpy as np
from sklearn.metrics import auc, precision_recall_curve, roc_curve
from sklearn.linear_model import LogisticRegression
from utils.calcs import calculate_bedroc, calculate_enrichment_factor, bedroc_score
from utils.putils import scale, num_derivative

# Constants
FORMATS = {"csv": pd.read_csv, "excel": pd.read_excel}
MODEL = LogisticRegression(solver="lbfgs", penalty=None)

# Functions
def read(file: str):
    format_func = FORMATS["excel"] if file.endswith((".xlsx", ".ods")) else FORMATS["csv"]
    return format_func(file, sep=None, engine='python')

def fit_predict(x, y):
    x = x.reshape(-1, 1)
    clf = MODEL.fit(x, y)
    predictions = clf.predict_proba(x)[:, 1]
    return predictions

def generate_percentiles(predictions):
    percentiles = np.arange(1, len(predictions) + 1) / len(predictions)
    return percentiles

def preprocess_data(df):
    df = df.dropna(axis=1, how='all')

    cols = df.columns
    scores = df[cols[0]].values
    actives = df[cols[1]].values

    return np.array(scores), np.array(actives)

def generate_precision_recall(predictions, activity):
    precision, recall, thresholds = precision_recall_curve(activity, predictions)
    return precision, recall, thresholds
    

def calculate_curves(program_name, scores, activity):
    """
    Calculates ROC, precision-recall, and BEDROC along with percentile enrichment data.
    
    Args:
        program_name: A string representing the name of the program (not used directly).
        scores: A numpy array of prediction scores.
        activity: A numpy array of binary labels (1 for active compounds, 0 for decoys).
    
    Returns:
        A dictionary containing ROC, precision-recall, BEDROC, and percentile enrichment data.
    """
 # Fit and predict (assuming fit_predict ranks scores by likelihood)
    predictions = fit_predict(scores, activity)  # Assuming this gives probabilities
    
    # Sort predictions in decreasing order and align the activity labels accordingly
    sorted_indices = np.argsort(-predictions)  # Negative sign to sort in descending order
    sorted_predictions = predictions[sorted_indices]
    sorted_activity = activity[sorted_indices]
    ranked_indices = np.arange(len(sorted_activity))  # Assuming rank positions
    # ROC curve calculation
    fpr, tpr, thresholds = roc_curve(sorted_activity[::-1], sorted_predictions[::-1], pos_label=1)
    roc_auc = auc(fpr, tpr)

    # Step 3: Generate percentile data for enrichment factors
    pc_x = generate_percentiles(predictions[sorted_indices[::-1]])
    n_actives = sum(activity)
    enrichment_factors = [calculate_enrichment_factor(activity, predictions, 1-x) for x in pc_x]

    # Step 4: Calculate BEDROC score
    bedroc = bedroc_score(activity, predictions)

    # Step 5: Prepare ROC data
    roc_data = {
        "x": fpr,
        "y": tpr,
        "auc": roc_auc,
        "thresholds": thresholds,
        "bedroc": bedroc
    }

    # Step 6: Prepare percentile enrichment data
    pc_y = predictions[sorted_indices[::-1]]
    prevalence = n_actives / len(activity)
    pc_data = {
        "x": pc_x,
        "y": pc_y,
        "avg_score": prevalence,
        "efs": enrichment_factors
    }

    # Step 7: Calculate precision-recall curve
    precision, recall, pr_thresholds = precision_recall_curve(activity, predictions)

    # Step 8: Return all calculated curves and data
    return {
        "roc": roc_data,
        "pc": pc_data,
        "precision_recall": {
            "x": recall,
            "y": precision,
            "thresholds": pr_thresholds
        }
    }

def calculate_selected_x(predictions):
    x_prime, y_hat_prime = num_derivative(generate_percentiles(predictions), predictions)
    x_prime, y_hat_prime = scale(x_prime), scale(y_hat_prime)

    threshold_idx = np.argmax(y_hat_prime > 0.34)
    return x_prime[threshold_idx]
