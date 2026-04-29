import streamlit as st
import warnings

from pages.auth import render_login, logout
from pages.admin import render_admin_panel
from pages.dashboard import render_dashboard
from pages.upload import render_upload
from pages.training_config import render_training_config
from pages.training import render_training
from pages.analytics import render_analytics
from pages.threat_intel import render_threat_intel

warnings.filterwarnings('ignore')

def init_session_state():
    defaults = {
        'authenticated': False,
        'username': None,
        'role': None,
        'user_id': None,
        'current_page': 'login',
        'show_register': False,
        'token': None,
        'dataset_id': None,
        'training_config': {},
        'job_id': None,
        'model_id': None,
        'feature_names': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def main():
    st.set_page_config(
        page_title="SOC Anomaly Detection",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="collapsed" if not st.session_state.get('authenticated') else "expanded"
    )
    
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #1a1a2e);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #ffffff;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            margin-bottom: 1.5rem;
        }
        .login-container {
            max-width: 450px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 2rem;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .alert-critical {
            background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
            color: white;
            padding: 12px;
            border-radius: 8px;
            margin: 8px 0;
            border-left: 4px solid #8b0000;
        }
        .alert-high {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 12px;
            border-radius: 8px;
            margin: 8px 0;
        }
        .alert-medium {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 12px;
            border-radius: 8px;
            margin: 8px 0;
        }
        .alert-low {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            color: white;
            padding: 12px;
            border-radius: 8px;
            margin: 8px 0;
        }
        .step-indicator {
            display: flex;
            justify-content: center;
            margin: 20px 0;
            align-items: center;
        }
        .step {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: rgba(255,255,255,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 10px;
            font-weight: bold;
            color: white;
            border: 2px solid rgba(255,255,255,0.3);
        }
        .step.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-color: white;
        }
        .step.completed {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            border-color: white;
        }
        .step-line {
            width: 60px;
            height: 3px;
            background: rgba(255,255,255,0.2);
        }
        .step-line.completed {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }
    </style>
    """, unsafe_allow_html=True)
    
    init_session_state()
    
    if not st.session_state.authenticated:
        render_login()
    else:
        page = st.session_state.current_page
        
        if page == 'admin':
            render_admin_panel()
        elif page == 'upload':
            render_upload()
        elif page == 'training_config':
            render_training_config()
        elif page == 'training':
            render_training()
        elif page == 'dashboard':
            render_dashboard()
        elif page == 'analytics':
            render_analytics()
        elif page == 'threat_intel':
            render_threat_intel()
        else:
            render_dashboard()

if __name__ == "__main__":
    main()