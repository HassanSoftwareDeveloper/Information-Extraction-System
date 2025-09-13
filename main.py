

"""
Event Registration Information Extraction System
Entry Point Module
"""

import streamlit as st
from frontend import ProfessionalEventExtractionInterface

def main() -> None:
    """Main application entry point."""
    try:
        app = ProfessionalEventExtractionInterface()
        app.run_application()  # Changed from run() to run_application()
    except Exception as e:
        st.error(f"Application failed to start: {str(e)}")
        st.stop()

if __name__ == "__main__":
    main()