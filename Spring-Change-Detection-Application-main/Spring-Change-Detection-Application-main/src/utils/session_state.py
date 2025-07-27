import streamlit as st

class SessionStateManager:
    """
    Manages Streamlit session state for the Spring Change Detection app.
    """

    DEFAULTS = {
        "input_excel_old": None,
        "input_excel_new": None,
        "old_uploaded": False,
        "results": None,
        "analysis_completed": False,
        "pta_type": None,
        "current_step": "upload",
    }

    @staticmethod
    def initialize():
        """Initialize session state keys with default values."""
        for key, default in SessionStateManager.DEFAULTS.items():
            if key not in st.session_state:
                st.session_state[key] = default

    @staticmethod
    def clear_all():
        """
        Clear all session state values except 'current_step',
        which resets to 'upload'.
        """
        for key in SessionStateManager.DEFAULTS:
            if key == "current_step":
                st.session_state[key] = "upload"
            else:
                st.session_state[key] = None

    @staticmethod
    def remove_results():
        """Remove analysis results from session state."""
        st.session_state["results"] = None

    @staticmethod
    def reset_workflow():
        """Reset the workflow to the initial upload step."""
        for key in ["input_excel_old", "input_excel_new", "results", "analysis_completed", "current_step"]:
            if key == "current_step":
                st.session_state[key] = "upload"
            elif key == "analysis_completed":
                st.session_state[key] = False
            else:
                st.session_state[key] = None
