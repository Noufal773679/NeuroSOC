import streamlit as st
from api_client import get_client

def render_threat_intel():
    st.markdown('<div class="main-header">THREAT INTELLIGENCE</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("Navigation")
        if st.button("Dashboard", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()
        if st.button("Analytics", use_container_width=True):
            st.session_state.current_page = 'analytics'
            st.rerun()
        if st.button("Threat Intel", use_container_width=True):
            st.session_state.current_page = 'threat_intel'
            st.rerun()
        
        if st.session_state.get('role') == 'admin':
            st.markdown("---")
            if st.button("Admin Panel", use_container_width=True):
                st.session_state.current_page = 'admin'
                st.rerun()
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            from pages.auth import logout
            logout()
    
    st.info("Threat Intelligence features require Association Rule Mining to be enabled during training.")
    st.write("After training with ARM enabled, attack signatures and frequent patterns will be displayed here.")
    
    st.subheader("Attack Signatures")
    st.warning("Association Rule Mining results will be available in a future update.")