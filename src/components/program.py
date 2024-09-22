import pandas as pd
from model.pydockstats import calculate_curves, preprocess_data

class Program:
    def __init__(self, name: str):
        self.name = name        
        self.__ligands = pd.DataFrame(data=[{'score': None}], columns=['score'])
        self.__decoys = pd.DataFrame(data=[{'score': None}], columns=['score'])

        self.__quantiles = None
        self.__probabilities = None
        self.__prevalence = None
        self.__enrichment_factors = None

        self.__fpr = None
        self.__tpr = None
        self.__auc = None
        self.__thresholds = None
        self.__bedroc = None

        self.__recall = None
        self.__precision = None
        self.__pr_thresholds = None

        self.data_generated = False
        self.data_inputted = False

    @property
    def quantiles(self):
        return self.__quantiles
    
    @property
    def probabilities(self):
        return self.__probabilities
    
    @property
    def prevalence(self):
        return self.__prevalence
    
    @property
    def enrichment_factors(self):
        return self.__enrichment_factors
    
    @property
    def fpr(self):
        return self.__fpr
    
    @property
    def tpr(self):
        return self.__tpr
    
    @property
    def auc(self):
        return self.__auc
    
    @property
    def bedroc(self):
        return self.__bedroc

    @property
    def recall(self):
        return self.__recall
    @property
    def precision(self):
        return self.__precision
    
    @property
    def thresholds(self):
        return self.__thresholds
    
    @property
    def pr_thresholds(self):
        return self.__pr_thresholds
    
    def set_data(self, ligands_score, decoys_score):
        self.__ligands = pd.DataFrame(data=ligands_score, columns=['score'])
        self.__decoys = pd.DataFrame(data=decoys_score, columns=['score'])
        self.data_inputted = True

    @property
    def ligands(self) -> pd.DataFrame:
        return self.__ligands
    
    @property
    def decoys(self) -> pd.DataFrame:
        return self.__decoys
    

    def generate(self):
        ligands_copy = self.__ligands.copy()
        decoys_copy = self.__decoys.copy()

        ligands_copy['activity'] = 1
        decoys_copy['activity'] = 0

        df = pd.concat([ligands_copy, decoys_copy], ignore_index=True)

        scores, activity = preprocess_data(df)

        curves = calculate_curves(self.name, scores, activity)
        
        pc = curves['pc']
        roc = curves['roc']
        precision_recall = curves['precision_recall']

        self.__quantiles = pc['x']
        self.__probabilities = pc['y']
        self.__prevalence = pc['avg_score']
        self.__enrichment_factors = pc['efs']

        self.__fpr = roc['x']
        self.__tpr = roc['y']
        self.__auc = roc['auc']
        self.__thresholds = roc['thresholds']
        self.__bedroc = roc['bedroc']

        self.__recall = precision_recall['x']
        self.__precision = precision_recall['y']
        self.__pr_thresholds = precision_recall['thresholds']

        self.data_generated = True

    def to_dict(self):
        return {
            'ligands': self.__ligands,
            'decoys': self.__decoys,
        }
    
    def from_dict(self, data: dict):
        self.__ligands = data['ligands']
        self.__decoys = data['decoys']

