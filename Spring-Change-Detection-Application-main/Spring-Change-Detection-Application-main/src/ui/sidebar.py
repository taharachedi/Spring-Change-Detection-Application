import streamlit as st
import streamlit.components.v1 as com

def render_sidebare():
    with st.sidebar:
        #TODO: Workflow navigation
        current_step = st.session_state.get("current_step","upload")
        st.markdown("### 🚀 Project Workflow")
        workflow_steps = [
            {
                'key': 'upload',
                'title': '📁 Upload Files',
                'description': 'Upload PTA Excel files',
                'icon': '📁'
            },
            {
                'key': 'analysis',
                'title': '🔍 Analysis and visualization 📈',
                'description': 'Perform analysis and visualization',
                'icon': '🔍'
            },
            {
                'key': 'results',
                'title': '📊 Results',
                'description': 'View result dataframe and download in excel file',
                'icon': '📊'
            },
        ]
        
        #TODO: Create the workflow buttons 
        for i, step in enumerate(workflow_steps):
            is_current = current_step == step['key']
            is_completed = is_step_completed(step['key'])
            
            # Determine button style
            if is_current:
                button_type = "primary"
                status_icon = "🔵"
            elif is_completed:
                button_type = "secondary"
                status_icon = "✅"
            else:
                button_type = "secondary"
                status_icon = "⚪"
            
            # Create button with status
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"<div style='font-size: 1.2rem; padding: 8px 0;'>{status_icon}</div>", 
                          unsafe_allow_html=True)
            
            with col2:
                button_key = f"step_{step['key']}_{i}"  # More unique key
                if st.button(
                    f"{step['title']}", 
                    key=button_key, 
                    type=button_type,
                    use_container_width=True,
                ):
                    st.session_state.current_step = step['key']
                    st.rerun()
        st.divider()

        #TODO: About Project
        st.markdown("### ℹ️ About Project")
        with st.expander("Project Details", expanded =False):
            st.markdown("""
                        This application compares two PTA Excel files to detect vehicle spring changes:
            
                        **Key Features:**
                        - 📊 Statistical Analysis
                        - 🔍 Change Detection  
                        - 📈 Data Visualization
                        - 📋 Results Dashboard
                        - 📥 Excel Export
                        
                        **Supported Files:**
                        - Old PTA Excel file
                        - New PTA Excel file
                        """)


def is_step_completed(step_key):
    """Check if a workflow step is completed"""
    if step_key == 'upload':    
        return  st.session_state["input_excel_old"] is not None and st.session_state["input_excel_new"] is not None
    elif step_key == 'analysis':
        return st.session_state.get('analysis_completed', False)
    elif step_key == 'results':
        return st.session_state.get('analysis_completed', False)
    return False
