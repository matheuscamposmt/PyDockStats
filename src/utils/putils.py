import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def scale(x: np.array) -> np.array:
    _max = x.max()
    new = x / _max

    return new


def num_derivative(x: np.array, y: np.array) -> np.array:
    yprime = np.diff(y) / np.diff(x)
    xprime = []

    for i in range(len(yprime)):
        xtemp = (x[i + 1] + x[i]) / 2
        xprime = np.append(xprime, xtemp)

    return xprime, yprime


# aux functions
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

formats = {"csv": pd.read_csv, "excel": pd.read_excel}
def read_result_file(file: str):
    if file.endswith((".xlsx", ".ods")):
        return formats["excel"](file)
    else:
        return formats["csv"](file, sep=None, engine='python')
    
def save_plots(pc_data, roc_data, names, save_path="."):
    # create the pc fig and the roc fig each with the programs plotted
    # save the figs to the save_path

    # pc fig
    fig_pc = plt.figure(figsize=(10, 10))
    ax_pc = fig_pc.add_subplot(111)
    ax_pc.set_title("Predictiveness Curve")
    ax_pc.set_xlabel("Quantile")
    ax_pc.set_ylabel("Activity probability")
    ax_pc.set_ylim([0, 1])
    ax_pc.set_xlim([0, 1])
    ax_pc.grid(True)

    # roc fig
    fig_roc = plt.figure(figsize=(10, 10))
    ax_roc = fig_roc.add_subplot(111)
    ax_roc.set_title("ROC (Receiver Operating Characteristic)")
    ax_roc.set_xlabel("False Positive Rate")
    ax_roc.set_ylabel("True Positive Rate")
    ax_roc.set_ylim([0, 1])
    ax_roc.set_xlim([0, 1])
    ax_roc.grid(True)

    # plot the data
    for i, name in enumerate(names):
        # pc
        x_pc, y_pc = pc_data[i]
        ax_pc.plot(x_pc, y_pc, label=name)

        # roc
        x_roc, y_roc = roc_data[i]
        ax_roc.plot(x_roc, y_roc, label=name)

    # save the figs
    fig_path = f"{save_path}/figs/pc.png"
    fig_pc.savefig(fig_path)

    roc_path = f"{save_path}/figs/roc.png"
    fig_roc.savefig(roc_path)

    return [fig_path, roc_path]

# Function to generate realistic artificial docking scores for ligands and decoys
def generate_artificial_scores(max_points: int = 1000):
    """
    Generate artificial docking scores that simulate the behavior of real-world docking data.

    Args:
        num_ligands: Number of ligands (actives) to generate.
        num_decoys: Number of decoys (inactive compounds) to generate.

    Returns:
        A dictionary containing the generated scores for ligands and decoys.
    """
    # random number of decoys (make it bigger than 0.5)
    frac_decoys = 0.5 + np.random.rand() * 0.3

    num_decoys = int(max_points * frac_decoys)  # Random number of decoys
    num_ligands = max_points - num_decoys  # Remaining points are ligands

    # Generate random docking scores for decoys and ligands
    # Decoys generally have worse (higher) scores than ligands, so we adjust the beta distribution
    decoys = -1 * (np.random.beta(2, 5, num_decoys) * 10 + np.random.normal(0, 0.5, num_decoys))  # Shift to negative range
    ligands = -1 * (np.random.beta(5, 2, num_ligands) * 8 + np.random.normal(0, 0.3, num_ligands))  # Better (lower) scores

    # add powerful noise
    decoys = decoys + np.random.normal(0, 2, num_decoys)
    ligands = ligands + np.random.normal(0, 2, num_ligands)

    # Introduce a few outliers (extremely good or bad scores)
    frac_outliers = 0.01 + np.random.rand() * 0.05  # Fraction of outliers
    n_outliers = int(max_points * frac_outliers)  # Number of outliers
    ligand_outliers = -1 * np.random.uniform(0, 5, n_outliers)  # Very low (good) scores for a few ligands
    ligands[:n_outliers] = ligand_outliers

    decoy_outliers = -1 * np.random.uniform(10, 20, n_outliers)  # Very high (bad) scores for a few decoys
    decoys[:n_outliers] = decoy_outliers

    # Create a DataFrame for easier manipulation and realistic output format
    data = {
        "decoys": decoys,
        "ligands": ligands
    }


    return data
