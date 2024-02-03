import pandas as pd
from pydockstats import calculate_curves, preprocess_data

class Program:
    def __init__(self, name: str):
        self.name = name        
        self.__ligands = pd.DataFrame(data=[{'score': None}], columns=['score'])
        self.__decoys = pd.DataFrame(data=[{'score': None}], columns=['score'])

        self.__quantiles = None
        self.__probabilities = None

        self.__fpr = None
        self.__tpr = None
        self.__auc = None

        self.data_generated = False
        self.data_inputted = False

    @property
    def quantiles(self):
        return self.__quantiles
    
    @property
    def probabilities(self):
        return self.__probabilities
    
    @property
    def fpr(self):
        return self.__fpr
    
    @property
    def tpr(self):
        return self.__tpr
    
    @property
    def auc(self):
        return self.__auc
        
    def set_data(self, ligands, decoys):
        self.__ligands = ligands
        self.__decoys = decoys
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

        df = pd.concat([ligands_copy, decoys_copy], ignore_index=True).sample(frac=1)

        scores, activity = preprocess_data(df)

        pc, roc = calculate_curves(self.name, scores, activity)

        self.__quantiles = pc['x']
        self.__probabilities = pc['y']

        self.__fpr = roc['x']
        self.__tpr = roc['y']
        self.__auc = roc['auc']

        self.data_generated = True

