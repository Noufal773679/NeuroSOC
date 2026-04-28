import streamlit as st
from api_client import get_client

def render_login():
    st.markdown('<div class="main-header">SOC COMMAND CENTER</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: white; font-size: 1.1rem; margin-bottom: 2rem;">Network Threat Detection & Analysis System</div>', unsafe_allow_html=True)
    
    client = get_client()
    
    # Check first run
    first_run = client.check_first_run()
    if first_run and first_run.get("first_run"):
        render_first_admin_setup()
        return
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("### Secure Login")
        
        username = st.text_input("Username", key="login_user", placeholder="Enter your username")
        password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("Login", use_container_width=True):
                if not username or not password:
                    st.error("Please fill in all fields")
                else:
                    result = client.login(username, password)
                    if result:
                        st.success("Login successful!")
                        st.session_state.current_page = 'upload' if result['role'] != 'admin' else 'admin'
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        
        with col_btn2:
            if st.button("Register", use_container_width=True):
                st.session_state.show_register = True
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.session_state.get('show_register', False):
            st.markdown('<div class="login-container" style="margin-top: 2rem;">', unsafe_allow_html=True)
            st.markdown("### Create New Account")
            
            new_username = st.text_input("Choose Username", key="reg_user", placeholder="Enter username")
            new_password = st.text_input("Choose Password", type="password", key="reg_pass", placeholder="Min 6 characters")
            confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Confirm password")
            
            role_options = ['analyst', 'student', 'other']
            role_display = ['Analyst', 'Student', 'Other']
            selected_role_idx = st.selectbox("Select Role", range(len(role_options)), format_func=lambda i: role_display[i])
            selected_role = role_options[selected_role_idx]
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Create Account", type="primary", use_container_width=True):
                    if not new_username or not new_password:
                        st.error("Please fill in all fields")
                    elif new_password != confirm_pass:
                        st.error("Passwords do not match")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        result = client.register(new_username, new_password, selected_role)
                        if result:
                            st.success("Account created! You can now login.")
                            st.session_state.show_register = False
                            st.rerun()
                        else:
                            st.error("Username already exists")
            
            with col2:
                if st.button("Back to Login", use_container_width=True):
                    st.session_state.show_register = False
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

def render_first_admin_setup():
    st.markdown('<div class="main-header">Welcome to SOC Command Center</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: white; font-size: 1.2rem; margin-bottom: 2rem;">Initial System Setup - Create Admin Account</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("### Create Administrator Account")
        st.markdown("<p style='color: #ff6b6b; font-size: 0.9rem;'>This is a one-time setup. Please create your admin credentials carefully.</p>", unsafe_allow_html=True)
        
        admin_username = st.text_input("Admin Username", placeholder="Enter admin username")
        admin_password = st.text_input("Password", type="password", placeholder="Enter strong password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
        
        if st.button("Create Admin Account", type="primary", use_container_width=True):
            if not admin_username or not admin_password:
                st.error("Please fill in all fields")
            elif admin_password != confirm_password:
                st.error("Passwords do not match")
            elif len(admin_password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                client = get_client()
                result = client.first_admin(admin_username, admin_password)
                if result:
                    st.success("Admin account created! Please login.")
                    st.rerun()
                else:
                    st.error("Failed to create admin account")
        
        st.markdown("</div>", unsafe_allow_html=True)

def logout():
    client = get_client()
    client.logout()