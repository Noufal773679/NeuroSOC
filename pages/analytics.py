import streamlit as st
import plotly.express as px
from api_client import get_client

def render_analytics():
    st.markdown('<div class="main-header">ADVANCED ANALYTICS</div>', unsafe_allow_html=True)
    
    if 'model_id' not in st.session_state:
        st.warning("No prediction data available. Please complete training first.")
        return
    
    client = get_client()
    model_id = st.session_state.model_id
    
    with st.spinner("Loading analytics..."):
        predictions = client.get_predictions(model_id)
    
    if not predictions:
        st.error("Failed to load analytics data")
        return
    
    # Sidebar
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
    
    # Metrics
    metrics = predictions.get('metrics', {})
    if metrics:
        st.subheader("Model Performance")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Accuracy", f"{metrics.get('accuracy', 0):.4f}")
        col2.metric("Precision", f"{metrics.get('precision', 0):.4f}")
        col3.metric("Recall", f"{metrics.get('recall', 0):.4f}")
        col4.metric("F1-Score", f"{metrics.get('f1', 0):.4f}")
        col5.metric("ROC-AUC", f"{metrics.get('roc_auc', 0):.4f}")
    
    # Confusion matrix data
    st.subheader("Classification Results")
    col1, col2 = st.columns(2)
    with col1:
        tp = metrics.get('true_positives', 0)
        tn = metrics.get('true_negatives', 0)
        fp = metrics.get('false_positives', 0)
        fn = metrics.get('false_negatives', 0)
        
        st.write("**Confusion Matrix:**")
        st.write(f"True Positives: {tp}")
        st.write(f"True Negatives: {tn}")
        st.write(f"False Positives: {fp}")
        st.write(f"False Negatives: {fn}")
    
    with col2:
        total = predictions.get('total_samples', 0)
        attacks = predictions.get('attack_count', 0)
        benign = predictions.get('benign_count', 0)
        
        fig = px.pie(
            values=[attacks, benign],
            names=['Attacks', 'Benign'],
            title='Prediction Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Download
    st.subheader("Export Data")
    download_url = client.download_results(model_id)
    st.markdown(f"[📥 Download Full Predictions CSV]({download_url})")