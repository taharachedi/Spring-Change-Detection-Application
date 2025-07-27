import streamlit as st

from config import PAGE_TITLE, PAGE_ICON, PAGE_LAYOUT, INITIAL_SIDEBAR_STATE
from ui.sidebar import render_sidebare
from ui.uploads import render_upload_section
from ui.analysis import render_analysis
from ui.results import Result
from utils.session_state import SessionStateManager
from ui.styles import STYLES
import streamlit.components.v1 as com
from data_processing import generate_results_df

def render_hero_section():
    # project title
    col1,col2 = st.columns([10,4], gap="small")
    with col1:
        st.markdown(f"<h1 style='{STYLES['center_heading']}'>{PAGE_TITLE}</h1>", unsafe_allow_html=True)
        
    with col2:
        com.iframe(
            "https://lottie.host/embed/d21bd171-203a-4af2-9804-fc8b44bddf07/Pz8o5DauIj.lottie",
            height = 100,
            width = 100
        )
    
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        com.iframe(
            "https://lottie.host/embed/c8bdced2-de93-4f7f-bf2d-91321f0b6642/6oO7ycLrSJ.lottie",
            height=500,
            width=500,
        )

def render_main_content():
    """Render the main content based on current step"""
    
    # Get current step from session state
    current_step = st.session_state.get('current_step', 'upload')
    
    if current_step == 'upload':
        st.markdown("### 📁 Step 1: Upload Your Excel Files")
        st.markdown("Please upload both the old and new PTA Excel files to begin the analysis.")
        
        # Render upload section
        render_upload_section()
        
        # Check if files are uploaded and show status
        old_file = st.session_state.get('input_excel_old')
        new_file = st.session_state.get('input_excel_new')
        
        if old_file is not None and new_file is not None:
            st.success("✅ Both files uploaded successfully! You can now proceed to analysis.")
            
            if st.button("🔍 Proceed to Analysis", type="primary"):
                st.session_state.current_step = 'analysis'
                st.rerun()
        elif old_file is not None or new_file is not None:
            st.info("📋 Please upload both files to proceed.")
        
    elif current_step == 'analysis':
        st.markdown("### 🔍 Step 2: Perform Analysis")
        
        # Check if files are uploaded before analysis
        old_file = st.session_state.get('input_excel_old')
        new_file = st.session_state.get('input_excel_new')
        
        if old_file is None or new_file is None:
            st.warning("⚠️ Please upload both files first.")
            if st.button("🔙 Go Back to Upload"):
                st.session_state.current_step = 'upload'
                st.rerun()
        else:
            # Check if analysis is already completed
            if st.session_state.get('analysis_completed', False):
                st.success("✅ Analysis already completed!")
                if st.button("🔄 Re-run Analysis"):
                    st.session_state.analysis_completed = False
                    st.rerun()
                if st.button("📊 View Results", type="primary"):
                    st.session_state.current_step = 'results'
                    st.rerun()
            else:
                # Perform analysis
                with st.spinner("Performing analysis..."):
                    try:
                        render_analysis()
                        
                        # Mark analysis as completed
                        st.session_state.analysis_completed = True
                        st.success("✅ Analysis completed successfully!")
                        
                        # Auto-advance option
                        if st.button("📊 View Results", type="primary"):
                            st.session_state.current_step = 'results'
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
                        st.session_state.analysis_completed = False
        
    elif current_step == 'results':
        st.markdown("### 📊 Step 3: Analysis Results")
        st.markdown("Here are your comprehensive analysis results:")
        
        if st.session_state.get('analysis_completed', False):
            try:
                Result().display_results()
                
                # Success message
                st.success("✅ Results displayed successfully! You can now download your results.")
                
                # Action buttons
                if st.button("📁 Upload New Files"):
                    st.session_state.input_excel_old = None
                    st.session_state.input_excel_new = None
                    st.session_state.analysis_completed = False
                    st.session_state.current_step = 'upload'
                    st.rerun()
                        
            except Exception as e:
                st.error(f"❌ Error displaying results: {str(e)}")
                if st.button("🔙 Go Back to Analysis"):
                    st.session_state.current_step = 'analysis'
                    st.rerun()
        else:
            st.warning("⚠️ Please complete the analysis first.")
            if st.button("🔙 Go Back to Analysis"):
                st.session_state.current_step = 'analysis'
                st.rerun()
    
def main():
    # Set page configuration FIRST
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=PAGE_LAYOUT,
        initial_sidebar_state=INITIAL_SIDEBAR_STATE
    )
    
    # Initialize session states
    session = SessionStateManager
    session.initialize()

    # Initialize current step if not exists
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'upload'
    current_step = st.session_state.get('current_step', 'upload')
    # Render hero section
    if current_step == '':
        render_hero_section()
    
    # Render sidebar with workflow
    render_sidebare()
    
    old_df = st.session_state.get('input_excel_old')
    new_df = st.session_state.get('input_excel_new')
    pta_type = st.session_state.get('pta_type')
    
    # Create result dataframe only if both files are uploaded
    if (old_df is not None and 
        new_df is not None):
        try:
            generate_results_df(old_df,new_df,pta_type)
        except Exception as e:
            st.error(f"Error creating result dataframe: {str(e)}")
    
    # Render main content
    render_main_content()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 20px; color: #666; border-top: 1px solid #eee; margin-top: 40px;">
        <p>🔬 Vehicle Spring Analysis Tool | Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
