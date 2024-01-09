import pandas as pd
class Program:
    def __init__(self, name: str):
        self.name = name        
        self.__ligands_df = pd.DataFrame(data=[{'score': None}], columns=['score'])
        self.__decoys_df = pd.DataFrame(data=[{'score': None}], columns=['score'])
    
    def set_ligands_df(self, data: pd.DataFrame):
        self.__ligands_df = data
    
    def set_decoys_df(self, data: pd.DataFrame):
        self.__decoys_df = data

    def get_data(self):
        return self.__ligands_df.copy(), self.__decoys_df.copy()
