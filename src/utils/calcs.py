import numpy as np

def optimal_threshold(fpr, tpr, thresholds):
    # selecting the optimal threshold based on ROC
    selected_t = thresholds[np.argmin(np.abs(fpr + tpr - 1))]

    return selected_t

def calculate_hits(y_true_sorted, idx_selected_t, activity):
    activity_topx = np.array(y_true_sorted[int(idx_selected_t):])


    hits_x = np.squeeze(np.where(activity_topx == 1)).size
    hits_t = np.squeeze(np.where(np.array(activity) == 1)).size

    return hits_x, hits_t

# Enrichment Factor
def calculate_EF(hits_x, hits_t, topx_percent):
    return (hits_x) / (hits_t * topx_percent)

# Total Gain
def calculate_TG(y_hat, p):
    return sum(abs(y_hat - p) / len(y_hat)) / (2 * p * (1 - p))

# Partial total gain from the selected threshold
def calculate_pTG(y_hat, idx_selected_t, p):
    return sum(abs(y_hat[idx_selected_t:] - p) / len(y_hat[idx_selected_t:])) / (
        2 * p * (1 - p)
    )

def calculate_enrichment_factor(y_true, y_pred, top_percentage=0.05):
    """
    Calcula o Fator de Enriquecimento (EF) em uma dada porcentagem superior
    da lista classificada.

    Args:
        y_true (array_like): Rótulos de classe binária. 1 para classe positiva,
        0 caso contrário.
        y_pred (array_like): Valores de previsão.
        top_percentage (float): A porcentagem superior da lista classificada
        para a qual calcular o EF.

    Returns:
        float: O Fator de Enriquecimento (EF).
    """
    assert len(y_true) == len(y_pred), \
        'O número de pontuações deve ser igual ao número de rótulos.'

    # Classifica os valores de previsão em ordem decrescente
    sorted_indices = np.argsort(y_pred)[::-1]
    sorted_y_true = y_true[sorted_indices]

    # Calcula o ponto de corte para a porcentagem superior
    cutoff = int(len(y_true) * top_percentage)

    # Calcula o número de ativos na porcentagem superior
    top_actives = np.sum(sorted_y_true[:cutoff])

    print("Top Actives:", top_actives)
    print("Total Actives:", np.sum(y_true))
    print("Cutoff:", cutoff)
    print("Total:", len(y_true))

    # Calcula o EF
    ef = (top_actives / np.sum(y_true)) / (cutoff / len(y_true))

    return ef

def calculate_bedroc(ranks: np.ndarray, n_actives: int, R: float = 20.0) -> float:
  """
  Calculates the Boltzmann-enhanced discrimination of ROC (BEDROC) metric.

  Args:
    ranks: A numpy array containing the ranks of all compounds (actives and decoys).
    n_actives: The total number of active compounds.
    R: The exponential factor (default: 20.0).

  Returns:
    The BEDROC score (a value between 0 and 1).
  """
  N = len(ranks)  # Total number of compounds
  Ra = n_actives / N  # Ratio of actives

  # Calculate the numerator of the BEDROC formula (Eq. 36 in the source)
  numerator = np.sum(np.exp(-R * ranks[:n_actives] / N)) / (n_actives * (1 - np.exp(-R)) / (np.exp(R/N) - 1))

  # Calculate the denominator (normalization factor in Eq. 36)
  denominator = (Ra * np.sinh(R/2)) / (np.cosh(R/2) - np.cosh(R/2 - R*Ra)) + 1 / (1 - np.exp(-R*(1-Ra)))

  return numerator / denominator


def bedroc_score(y_true, y_pred, decreasing=True, alpha=20.0):
    """Métrica BEDROC implementada de acordo com Truchon e Bayley.

    O Boltzmann Enhanced Descrimination of the Receiver Operator 
    Characteristic (BEDROC) score é uma modificação do Receiver Operator 
    Characteristic (ROC) score que permite um fator de *reconhecimento 
    precoce*.

    Referências:
        O artigo original de Truchon et al. está localizado em 
        `10.1021/ci600426e 
        <http://dx.doi.org/10.1021/ci600426e>`_.

    Args:
        y_true (array_like):
            Rótulos de classe binária. 1 para classe positiva, 0 caso contrário.
        y_pred (array_like):
            Valores de previsão.
        decreasing (bool):
            True se valores altos de ``y_pred`` estiverem correlacionados à 
            classe positiva.
        alpha (float):
            Parâmetro de reconhecimento precoce.

    Returns:
        float:
            Valor no intervalo [1] indicando o grau em que a técnica 
            preditiva empregada detecta (previamente) a classe positiva.
    """
    assert len(y_true) == len(y_pred), \
        'O número de pontuações deve ser igual ao número de rótulos'
    big_n = len(y_true)
    n = sum(y_true == 1)
    if decreasing:
        order = np.argsort(-y_pred)
    else:
        order = np.argsort(y_pred)
    m_rank = (y_true[order] == 1).nonzero()[0]
    s = np.sum(np.exp(-alpha * m_rank / big_n))
    r_a = n / big_n

    # Calcular RIE_min e RIE_max usando as fórmulas corretas
    if alpha * r_a < 1:
        rie_min = alpha * np.exp(alpha - 1)
        rie_max = alpha / (1 - np.exp(-alpha))
    else:
        rie_min = (1 - np.exp(alpha * r_a)) / (r_a * (1 - np.exp(alpha)))
        rie_max = (1 - np.exp(-alpha * r_a)) / (r_a * (1 - np.exp(-alpha)))

    # Calcular RIE
    rand_sum = r_a * (1 - np.exp(-alpha))/(np.exp(alpha/big_n) - 1)
    rie = s / rand_sum

    # Calcular BEDROC usando RIE, RIE_min e RIE_max
    bedroc = (rie - rie_min) / (rie_max - rie_min)

    return bedroc