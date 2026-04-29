import streamlit as st
from api_client import get_client

def render_training_config():
    st.markdown('<div class="main-header">TRAINING CONFIGURATION</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="step-indicator">
        <div class="step completed">✓</div>
        <div class="step-line completed"></div>
        <div class="step active">2</div>
        <div class="step-line"></div>
        <div class="step">3</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Configure Model Parameters")
    
    if 'dataset_id' not in st.session_state:
        st.warning("No dataset uploaded. Please upload data first.")
        if st.button("Go to Upload"):
            st.session_state.current_page = 'upload'
            st.rerun()
        return
    
    dataset_id = st.session_state.dataset_id
    
    with st.form("training_config_form"):
        st.subheader("MSCA Configuration")
        col1, col2 = st.columns(2)
        with col1:
            use_msca = st.checkbox("Enable MSCA (Multi-Sketch Projection)", value=True)
            n_sketches = st.slider("Number of Sketches", 2, 10, 5, 1) if use_msca else 5
        with col2:
            sketch_dim = st.slider("Sketch Dimension", 16, 64, 32, 8) if use_msca else 32
        
        st.subheader("Model Architecture")
        col1, col2, col3 = st.columns(3)
        with col1:
            latent_dim = st.slider("Latent Dimension", 16, 128, 32, 8)
        with col2:
            hidden_dims_str = st.text_input("Hidden Layers (comma-separated)", "128,64")
        with col3:
            dropout = st.slider("Dropout Rate", 0.0, 0.5, 0.1, 0.05)
        
        st.subheader("Loss Configuration")
        col1, col2 = st.columns(2)
        with col1:
            alpha = st.slider("CLAD vs SVDD Weight (α)", 0.0, 1.0, 0.5, 0.1)
        with col2:
            nu = st.slider("Outlier Fraction (ν)", 0.01, 0.2, 0.05, 0.01)
        
        st.subheader("Training Parameters")
        col1, col2, col3 = st.columns(3)
        with col1:
            epochs = st.slider("Training Epochs", 10, 200, 50, 10)
        with col2:
            batch_size = st.selectbox("Batch Size", [128, 256, 512, 1024], index=1)
        with col3:
            lr = st.selectbox("Learning Rate", [1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 5e-2], index=2)
        
        st.subheader("Detection Parameters")
        col1, col2 = st.columns(2)
        with col1:
            contamination = st.slider("Expected Contamination", 0.01, 0.2, 0.05, 0.01)
        with col2:
            enable_arm = st.checkbox("Enable Association Rule Mining", value=True)
        
        st.subheader("Association Rule Mining (Optional)")
        if enable_arm:
            col1, col2 = st.columns(2)
            with col1:
                min_support = st.slider("Min Support", 0.001, 0.1, 0.01, 0.001)
            with col2:
                min_confidence = st.slider("Min Confidence", 0.1, 0.9, 0.5, 0.05)
        else:
            min_support = 0.01
            min_confidence = 0.5
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("Start Training", type="primary", use_container_width=True)
    
    if submitted:
        st.session_state.training_config = {
            'use_msca': use_msca,
            'n_sketches': n_sketches,
            'sketch_dim': sketch_dim,
            'latent_dim': latent_dim,
            'hidden_dims': [int(x.strip()) for x in hidden_dims_str.split(",")],
            'dropout': dropout,
            'alpha': alpha,
            'nu': nu,
            'epochs': epochs,
            'batch_size': batch_size,
            'lr': lr,
            'contamination': contamination,
            'enable_arm': enable_arm,
            'min_support': min_support,
            'min_confidence': min_confidence
        }
        st.session_state.current_page = 'training'
        st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Upload"):
            st.session_state.current_page = 'upload'
            st.rerun()
    with col2:
        if st.button("Logout"):
            from pages.auth import logout
            logout()
    
    with st.sidebar:
        st.header("Session Info")
        st.write(f"User: **{st.session_state.get('username', 'N/A')}**")
        st.write(f"Role: **{st.session_state.get('role', 'N/A')}**")
        
        if st.session_state.get('role') == 'admin':
            st.markdown("---")
            if st.button("⚙️ Admin Panel", use_container_width=True):
                st.session_state.current_page = 'admin'
                st.rerun()