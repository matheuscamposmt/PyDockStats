import streamlit as st
import app_utils as utils
from docking_load import load_file
import pandas as pd
from pydockstats import preprocess_data

def input_programs(max=15):
    program_name_container = st.container()
    with program_name_container:
        name_program = st.text_input("Enter the name of the program (optional)", placeholder="Autodock Vina", 
                                     max_chars=30, value="", key='program_name')
        add_program = st.button("Add program", help="Add a new program tab", 
                                type='secondary', disabled=len(st.session_state.programs) > max)
        if add_program and name_program not in st.session_state.programs:
            if name_program:
                st.session_state.programs.append(name_program)
            else:
                program_name = f"Program {len(st.session_state.programs)+1}"
                st.session_state.programs.append(program_name)
            
def _program_tab_content(program_name):
    col1, col2 = st.columns([4, 1], gap='medium')
    with col1:
        st.subheader(f"Paste or upload the ligands and decoys scores for '{program_name}'")

    with col2:
        remove_program = st.button("Remove program", key=f'remove_{program_name}_tab', 
                                   type='primary', help="Remove this program tab",
                                   disabled=len(st.session_state.programs) <= 1)
        
    ligand_col, decoy_col = st.columns(2)
    with ligand_col:
        st.markdown("#### Ligands")
        data = pd.DataFrame(data=[{'score':None}], columns=['score'])
        ligand_data_editor = st.data_editor(data, num_rows="dynamic", 
                                            key=f"{program_name}_ligands_editor",
                                            width=300, column_config={
                                                'score': st.column_config.NumberColumn(
                                                    "Scores of the ligands"
                                                )
                                            })
        ligands_df = ligand_data_editor
    with decoy_col:
        st.markdown("#### Decoys")
        decoy_data_editor = st.data_editor(pd.DataFrame(data=[{'score':None}], columns=['score']), 
                                            num_rows="dynamic", key=f"{program_name}_decoys_editor",
                                            width=300, column_config={
                                                'score': st.column_config.NumberColumn(
                                                        "Scores of the decoys"
                                                )
                                                })
        decoys_df = decoy_data_editor
        
    upload_space = st.expander("Upload Files", expanded=False)
    with upload_space:
        # Upload files and display data preview
        ligands_file, decoys_file= utils.upload_files(program_name)
        if ligands_file or decoys_file:
            ligands_df = load_file(ligands_file)
            decoys_df = load_file(decoys_file)

    generate_button = st.button("Generate", key=f"generate_{program_name}_tab", 
                                use_container_width=True, type='primary', help="Generate the performance metric figures")
    if generate_button:
        ligands_df['activity'] = 1
        decoys_df['activity'] = 0
        # Combine ligands and decoys data into a single dataframe
        df = pd.concat([ligands_df, decoys_df], ignore_index=True).sample(frac=1)

        # Preprocess the combined data
        scores, activity = preprocess_data(df)

        # store data of the program in session state
        st.session_state.data[program_name] = dict(scores=scores, activity=activity)

    if remove_program:
        # remove the program from session state
        st.session_state.programs.remove(program_name)
        del remove_program
        try:
            del st.session_state.data[program_name] 
        except KeyError:
            pass
        st.rerun()

def generate_tabs():
    # User can "create" tabs when adding programs
    if st.session_state['programs']:
        programs_tabs = st.tabs(st.session_state.programs)
        for i in range(len(programs_tabs)):
            with programs_tabs[i]:
                _program_tab_content(st.session_state.programs[i])