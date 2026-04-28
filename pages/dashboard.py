import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from api_client import get_client

def render_dashboard():
    st.markdown('<div class="main-header">SOC COMMAND CENTER</div>', unsafe_allow_html=True)
    
    if 'model_id' not in st.session_state:
        st.warning("No trained model found. Please complete training first.")
        
        with st.sidebar:
            st.header("Navigation")
            if st.button("Upload Data", use_container_width=True):
                st.session_state.current_page = 'upload'
                st.rerun()
            if st.button("Logout", use_container_width=True):
                from pages.auth import logout
                logout()
        return
    
    client = get_client()
    model_id = st.session_state.model_id
    
    # Fetch stats from backend
    with st.spinner("Loading dashboard data..."):
        stats = client.get_stats(model_id)
    
    if not stats:
        st.error("Failed to load dashboard data")
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
            st.markdown("<p style='color: #ff6b6b; font-weight: bold;'>⚙️ ADMIN CONTROLS</p>", unsafe_allow_html=True)
            if st.button("Admin Panel", use_container_width=True):
                st.session_state.current_page = 'admin'
                st.rerun()
        
        st.markdown("---")
        st.header("Session Info")
        st.write(f"User: **{st.session_state.get('username', 'N/A')}**")
        st.write(f"Role: **{st.session_state.get('role', 'N/A')}**")
        
        st.markdown("---")
        st.header("Model Stats")
        st.write(f"Total Samples: {stats.get('total_samples', 0):,}")
        st.write(f"Detected Attacks: {stats.get('total_attacks', 0):,}")
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            from pages.auth import logout
            logout()
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["Real-time Monitoring", "Attack Distribution", "System Health"])
    
    with tab1:
        # Header stats
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Critical", stats.get('critical', 0), delta_color="inverse")
        with col2:
            st.metric("High", stats.get('high', 0), delta_color="inverse")
        with col3:
            st.metric("Medium", stats.get('medium', 0))
        with col4:
            st.metric("Low", stats.get('low', 0))
        with col5:
            threat_level = 'CRITICAL' if stats.get('critical', 0) > 10 else 'HIGH' if stats.get('high', 0) > 20 else 'MEDIUM' if stats.get('total_attacks', 0) > 50 else 'LOW'
            color = {'LOW': 'green', 'MEDIUM': 'orange', 'HIGH': 'red', 'CRITICAL': 'darkred'}[threat_level]
            st.markdown(f"""
            <div style="background-color: {color}; padding: 10px; border-radius: 5px; text-align: center; color: white; font-weight: bold;">
                THREAT LEVEL<br>{threat_level}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Attack alerts
        st.subheader("Recent Alerts")
        attack_types = stats.get('attack_types', {})
        if attack_types:
            for attack_type, count in list(attack_types.items())[:10]:
                severity = 'HIGH' if count > 50 else 'MEDIUM' if count > 20 else 'LOW'
                alert_class = f"alert-{severity.lower()}"
                st.markdown(f"""
                <div class="{alert_class}">
                    <strong>[{severity}]</strong> {attack_type}: {count} detections
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No attacks detected")
    
    with tab2:
        attack_types = stats.get('attack_types', {})
        if attack_types:
            fig = px.pie(
                values=list(attack_types.values()),
                names=list(attack_types.keys()),
                title='Detected Attack Types Distribution',
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No attack data available")
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Anomaly Score", f"{stats.get('avg_score', 0):.4f}")
        with col2:
            st.metric("Max Anomaly Score", f"{stats.get('max_score', 0):.4f}")
        
        # Download button
        download_url = client.download_results(model_id)
        st.markdown(f"[Download Full Results CSV]({download_url})")