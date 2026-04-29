import streamlit as st
import time
from api_client import get_client

def render_training():
    st.markdown('<div class="main-header">MODEL TRAINING</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="step-indicator">
        <div class="step completed">✓</div>
        <div class="step-line completed"></div>
        <div class="step completed">✓</div>
        <div class="step-line completed"></div>
        <div class="step active">3</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Training in Progress")
    
    if 'training_config' not in st.session_state or 'dataset_id' not in st.session_state:
        st.warning("Training configuration not found. Please start from upload.")
        if st.button("Go to Upload"):
            st.session_state.current_page = 'upload'
            st.rerun()
        return
    
    client = get_client()
    config = st.session_state.training_config
    dataset_id = st.session_state.dataset_id
    
    if "job_id" not in st.session_state:
        with st.spinner("Starting training on backend..."):
            result = client.start_training(dataset_id, config)
        
        if result and result.get("job_id"):
            st.session_state.job_id = result["job_id"]
            st.success(f"Training started! Job ID: {result['job_id']}")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Failed to start training. Please try again.")
            return
    
    job_id = st.session_state.job_id
    
    status_placeholder = st.empty()
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status = client.get_training_status(job_id)
    
    if not status:
        status_text.error("Could not retrieve training status")
        return
    
    if status.get("status") == "completed":
        progress_bar.progress(1.0)
        status_placeholder.success("✅ Training Complete!")
        
        metrics = status.get("metrics", {})
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Accuracy", f"{metrics.get('accuracy', 0):.4f}")
            col2.metric("Precision", f"{metrics.get('precision', 0):.4f}")
            col3.metric("Recall", f"{metrics.get('recall', 0):.4f}")
            col4.metric("F1-Score", f"{metrics.get('f1', 0):.4f}")
        
        st.session_state.model_id = status.get("model_id")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("View Dashboard", type="primary", use_container_width=True):
                st.session_state.current_page = 'dashboard'
                st.rerun()
        
    elif status.get("status") == "failed":
        progress_bar.empty()
        status_placeholder.error("❌ Training Failed")
        st.error(status.get("message", "Unknown error"))
        if st.button("Retry"):
            del st.session_state["job_id"]
            st.rerun()
    
    elif status.get("status") in ["queued", "running"]:
        progress = status.get("progress", 0)
        progress_bar.progress(min(1.0, progress))
        status_text.info(f"⏳ {status.get('message', 'Processing...')}")
        
        time.sleep(3)
        st.rerun()
    
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