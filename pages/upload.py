import streamlit as st
from api_client import get_client

def render_upload():
    st.markdown('<div class="main-header">DATA UPLOAD</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="step-indicator">
        <div class="step active">1</div>
        <div class="step-line"></div>
        <div class="step">2</div>
        <div class="step-line"></div>
        <div class="step">3</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Upload Network Traffic Data")
    
    uploaded_file = st.file_uploader("Upload CICIDS2017 CSV File", type=["csv"])
    
    if uploaded_file is not None:
        client = get_client()
        
        with st.spinner("Uploading and processing data..."):
            result = client.upload_csv(uploaded_file)
        
        if result:
            st.success(f"Uploaded successfully! Dataset ID: {result['dataset_id']}")
            st.info(f"Samples: {result['samples']:,} | Features: {result['features']}")
            
            with st.expander("Label Distribution"):
                st.write(result['labels'])
            
            st.session_state.dataset_id = result['dataset_id']
            st.session_state.feature_names = result['feature_names']
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Proceed to Training Configuration", type="primary", use_container_width=True):
                    st.session_state.current_page = 'training_config'
                    st.rerun()
        else:
            st.error("Upload failed. Please check your file and try again.")
    
    # Sidebar
    with st.sidebar:
        st.header("Session Info")
        st.write(f"User: **{st.session_state.get('username', 'N/A')}**")
        st.write(f"Role: **{st.session_state.get('role', 'N/A')}**")
        
        if st.session_state.get('role') == 'admin':
            st.markdown("---")
            if st.button("⚙️ Admin Panel", use_container_width=True):
                st.session_state.current_page = 'admin'
                st.rerun()
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            from pages.auth import logout
            logout()