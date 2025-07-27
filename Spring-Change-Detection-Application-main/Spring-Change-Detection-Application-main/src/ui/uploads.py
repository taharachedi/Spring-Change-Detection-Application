import streamlit as st
from file_handler import FileHandler
import pandas as pd
from config import UPLOAD_CONFIG

def render_upload_section():  
    # Prompt user to select PTA type (VP or VU) before file upload
    st.subheader("Select PTA Type:")
    pta_type = st.radio("PTA Type :", options=["VP", "VU"], index=0, horizontal=True)
    st.session_state['pta_type'] = pta_type
    
    col1, col2 = st.columns(2)
    
    with col1:
        _render_old_file()
                
    with col2:
        _render_new_file()
        
        
def _render_old_file():
        st.subheader("Old PTA file:")
        old_file = st.file_uploader(
            label = "Upload excel file only",
            type = UPLOAD_CONFIG["allowed_extension"],
            key = "old_file"
            )
        
        if old_file:
            _process_upload_file(old_file, "old", "input_excel_old")

@staticmethod 
def _render_new_file():
    st.subheader("New PTA file")
    new_file = st.file_uploader(
        label = "Upload excel file only",
        type = UPLOAD_CONFIG['allowed_extension'],
        key = "new_file"
        )
    if new_file:
        _process_upload_file(new_file, "new", "input_excel_new")

@staticmethod
def _process_upload_file(file, type_file, session_key):
    """
    - validate the excel file uploaded by the user 
    - if the excel is valid displaying the df and add the df to the session key
    - else display a commnet error returned from validate_excel_file
    """
    try:
        is_valid, comment, df = FileHandler.validate_excel_file(file, type_file)
        
        if is_valid: 
            st.success(f"✅ {type_file.title()} file uploaded seccussfully")
            
            #add the df to the session state
            st.session_state[session_key] = df
            
            # Store the original file object too for later use
            # Use a different name than the widget key to avoid conflicts
            st.session_state[type_file + '_file_object'] = file
                
            #displaying the df
            with st.expander(f"Preview {type_file.title()} File data"):
                st.dataframe(df)
        else:
            st.error(f"❌{comment}")
            st.session_state[session_key] = None
            # Use a different name than the widget key
            if type_file + '_file_object' in st.session_state:
                del st.session_state[type_file + '_file_object']
            
    except Exception as e:
        st.error(f"Error processing the {type_file.title()} file\n error:{str(e)}")
        st.session_state[session_key]= None
        # Use a different name than the widget key
        if type_file + '_file_object' in st.session_state:
            del st.session_state[type_file + '_file_object']