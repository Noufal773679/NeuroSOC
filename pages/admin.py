import streamlit as st
from api_client import get_client

def render_admin_panel():
    st.markdown('<div class="main-header">ADMIN CONTROL PANEL</div>', unsafe_allow_html=True)
    
    if st.session_state.get('role') != 'admin':
        st.error("Admin access required")
        return
    
    client = get_client()
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        if st.button("Dashboard", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()
        if st.button("Analytics", use_container_width=True):
            st.session_state.current_page = 'analytics'
            st.rerun()
        
        st.markdown("---")
        st.write(f"Logged in as: **{st.session_state.username}**")
        st.write(f"Role: **{st.session_state.role}**")
        st.markdown("---")
        
        if st.button("Logout", use_container_width=True):
            from pages.auth import logout
            logout()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["System Stats", "All Users", "Add User", "Password Reset"])
    
    with tab1:
        st.subheader("System Statistics")
        stats = client.get_system_stats()
        if stats:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Users", stats.get('total_users', 0))
            col2.metric("Online Users", stats.get('online_users', 0))
            col3.metric("Total Models", stats.get('total_models', 0))
            col4.metric("Total Results", stats.get('total_results', 0))
        else:
            st.error("Failed to load system stats")
    
    with tab2:
        st.subheader("All Registered Users")
        users = client.get_all_users()
        if users:
            st.dataframe(users, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.subheader("Delete User")
            
            usernames = [u['username'] for u in users if u['username'] != st.session_state.username]
            if usernames:
                col1, col2 = st.columns([3, 1])
                with col1:
                    user_to_delete = st.selectbox("Select User", usernames)
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("🗑️ Delete", type="secondary", use_container_width=True):
                        user_id = next(u['id'] for u in users if u['username'] == user_to_delete)
                        result = client.delete_user(user_id)
                        if result:
                            st.success(f"User '{user_to_delete}' deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete user")
            else:
                st.info("No other users to delete")
        else:
            st.warning("No users found")
    
    with tab3:
        st.subheader("Add New User")
        col1, col2, col3 = st.columns(3)
        with col1:
            new_username = st.text_input("Username", key="admin_new_user")
        with col2:
            new_password = st.text_input("Password", type="password", key="admin_new_pass")
        with col3:
            new_role = st.selectbox("Role", ["analyst", "student", "other"], key="admin_new_role")
        
        if st.button("Create User", type="primary"):
            if new_username and new_password and len(new_password) >= 6:
                result = client.create_user(new_username, new_password, new_role)
                if result:
                    st.success(f"User '{new_username}' created!")
                    st.rerun()
                else:
                    st.error("Failed to create user")
            else:
                st.error("Username required, password must be ≥6 chars")
    
    with tab4:
        st.subheader("Reset User Password")
        users = client.get_all_users()
        if users:
            reset_user = st.selectbox("Select User", [u['username'] for u in users], key="reset_user")
            new_pass = st.text_input("New Password", type="password", key="reset_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="reset_confirm")
            
            if st.button("Reset Password"):
                if new_pass == confirm_pass and len(new_pass) >= 6:
                    result = client.reset_password(reset_user, new_pass)
                    if result:
                        st.success(f"Password reset for '{reset_user}'")
                    else:
                        st.error("Failed to reset password")
                else:
                    st.error("Passwords must match and be ≥6 chars")
        else:
            st.warning("No users available")