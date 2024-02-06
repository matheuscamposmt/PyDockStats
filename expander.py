import streamlit as st
import pandas as pd
from program import Program
from typing import List, Dict

class ProgramExpander:
    count = 1
    def __init__(self, program: Program):
        self.id = ProgramExpander.count
        ProgramExpander.count += 1
        self.__program = program
        self.__remove_button = None

    @property
    def program(self) -> Program:
        return self.__program
    
    def is_remove_button_clicked(self) -> bool:
        return self.__remove_button

    def render(self):
        ligands_df, decoys_df = self.__program.ligands, self.__program.decoys
    
        col1, col2 = st.columns([4, 1])
        with col1:
            st.subheader(f"Paste the ligands and decoys scores for \"{self.__program.name}\" ")

        with col2:
            self.__remove_button = st.button("❌ Remove program", key=f'remove_{self.__program.name}_expander',
                                        type='secondary', help="Remove this program expander")

        ligand_col, decoy_col = st.columns([1, 1], gap='small')
        with ligand_col:
            st.markdown("#### Ligands")
            ligand_data_editor = st.data_editor(ligands_df, num_rows="dynamic",
                                                    key=f"{self.__program.name}_ligands_editor",
                                                    width=300, column_config={
                                                        'score': st.column_config.NumberColumn(
                                                            "Score of the ligands"
                                                        )
                                                    })
            ligands_df = ligand_data_editor

        with decoy_col:
            st.markdown("#### Decoys")
            decoy_data_editor = st.data_editor(decoys_df, num_rows="dynamic",
                                                key=f"{self.__program.name}_decoys_editor",
                                                width=300, column_config={
                                                    'score': st.column_config.NumberColumn(
                                                        "Score of the decoys"
                                                    )
                                                })
            decoys_df = decoy_data_editor
            
        if decoys_df['score'].isnull().any() or ligands_df['score'].isnull().any():
            st.warning("Please fill in all the scores")
            return


        self.__program.set_data(ligands_df, decoys_df)
    
    def data_inputted(self) -> bool:
        return self.__program.data_inputted
        
    def generate(self):
        self.__program.generate()



class ProgramsExpanders:
    def __init__(self, import_dict: dict = None):
        self.expanded = True
        if import_dict:
            self.expanded = False
            self.__expanders = []
            for name, data in import_dict.items():
                program = Program(name)
                program.set_data(data['ligands'], data['decoys'])
                self.__expanders.append(ProgramExpander(program))
        else:
            self.__expanders: List[ProgramExpander] = st.session_state['programs']

    @property
    def expanders(self) -> List[ProgramExpander]:
        return self.__expanders
    
    @property
    def programs(self) -> List[Program]:
        return [expander.program for expander in self.__expanders]
    
    @property
    def names(self) -> List[str]:
        return [expander.program.name for expander in self.__expanders]

    def add_program_expander(self, name: str):
        expander = ProgramExpander(Program(name))

        if expander.program.name not in self.names:
            self.__expanders.append(expander)

    def remove_expander(self, expander: ProgramExpander):
        self.__expanders.remove(expander)

        try:
            del st.session_state['data'][expander.program.name]
        except KeyError:
            pass
        st.rerun()

    def render(self):
        if self.__expanders:
            for expander in self.__expanders:
                with st.expander(expander.program.name, expanded=self.expanded):
                    expander.render()

                if expander.is_remove_button_clicked():
                    self.remove_expander(expander)

    def all_data_inputted(self) -> bool:
        if len(self.__expanders) == 0:
            return False
        return all([expander.data_inputted() for expander in self.__expanders])
    
    def all_data_generated(self) -> bool:
        bools = [expander.program.data_generated for expander in self.__expanders]
        if len(bools) == 0:
            return False
        return all([expander.program.data_generated for expander in self.__expanders])

    def generate(self):
        for expander in self.__expanders:
            expander.generate()

    def to_dict(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        return {program.name: program.to_dict() for program in self.programs}
        