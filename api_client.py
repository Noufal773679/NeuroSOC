import requests
import streamlit as st

BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:7860")

class APIClient:
    def __init__(self):
        self.base_url = BACKEND_URL.rstrip("/")
        self.token = st.session_state.get("token")
    
    def _get(self, endpoint, params=None):
        if params is None:
            params = {}
        params["token"] = self.token
        
        try:
            resp = requests.get(
                f"{self.base_url}{endpoint}", 
                params=params, 
                timeout=30
            )
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 403:
                return None  # Not admin, don't show error
            else:
                st.error(f"API Error {resp.status_code}: {resp.text}")
                return None
        except Exception as e:
            st.error(f"API Error: {str(e)}")
            return None
    
    def _post(self, endpoint, data=None, files=None):
        if data is None:
            data = {}
        
        try:
            if files:
                # File upload: token in form data
                form_data = {"token": self.token}
                if isinstance(data, dict):
                    form_data.update(data)
                
                resp = requests.post(
                    f"{self.base_url}{endpoint}", 
                    files=files, 
                    data=form_data,
                    timeout=120  # Longer timeout for uploads
                )
            else:
                # Regular POST: token in JSON
                if isinstance(data, dict):
                    data["token"] = self.token
                resp = requests.post(
                    f"{self.base_url}{endpoint}", 
                    json=data,
                    timeout=30
                )
            
            if resp.status_code in [200, 201]:
                return resp.json()
            else:
                st.error(f"API Error {resp.status_code}: {resp.text}")
                return None
        except Exception as e:
            st.error(f"API Error: {str(e)}")
            return None
    
    def _delete(self, endpoint, data=None):
        if data is None:
            data = {}
        data["token"] = self.token
        
        try:
            resp = requests.delete(
                f"{self.base_url}{endpoint}", 
                json=data, 
                timeout=30
            )
            if resp.status_code == 200:
                return resp.json()
            else:
                st.error(f"API Error {resp.status_code}: {resp.text}")
                return None
        except Exception as e:
            st.error(f"API Error: {str(e)}")
            return None
    
    # ==================== AUTH ====================
    def login(self, username, password):
        result = self._post("/auth/login", {"username": username, "password": password})
        if result:
            st.session_state.token = result["token"]
            st.session_state.user_id = result["user_id"]
            st.session_state.username = result["username"]
            st.session_state.role = result["role"]
            st.session_state.authenticated = True
        return result
    
    def register(self, username, password, role="analyst"):
        return self._post("/auth/register", {
            "username": username, 
            "password": password, 
            "role": role
        })
    
    def check_first_run(self):
        return self._get("/auth/check-first-run")
    
    def first_admin(self, username, password):
        return self._post("/auth/first-admin", {
            "username": username, 
            "password": password
        })
    
    def logout(self):
        if st.session_state.get("username"):
            self._post("/auth/logout", {"username": st.session_state.username})
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # ==================== UPLOAD ====================
    def upload_csv(self, file):
        files = {"file": (file.name, file.getvalue(), "text/csv")}
        return self._post("/upload/", files=files)
    
    # ==================== TRAINING ====================
    def start_training(self, dataset_id, config):
        return self._post("/train/start", {
            "dataset_id": dataset_id,
            "config": config
        })
    
    def get_training_status(self, job_id):
        return self._get(f"/train/status/{job_id}")
    
    # ==================== PREDICTIONS ====================
    def get_predictions(self, model_id):
        return self._get(f"/predictions/{model_id}")
    
    def get_stats(self, model_id):
        return self._get(f"/predictions/{model_id}/stats")
    
    def download_results(self, model_id):
        return f"{self.base_url}/predictions/{model_id}/download?token={self.token}"
    
    # ==================== ADMIN ====================
    def get_all_users(self):
        return self._get("/admin/users")
    
    def create_user(self, username, password, role):
        return self._post("/admin/users/create", {
            "target_username": username,
            "new_password": password,
            "new_role": role
        })
    
    def delete_user(self, user_id):
        return self._delete(f"/admin/users/{user_id}")
    
    def reset_password(self, username, new_password):
        return self._post("/admin/users/reset-password", {
            "target_username": username,
            "new_password": new_password
        })
    
    def get_system_stats(self):
        return self._get("/admin/stats")

def get_client():
    if "api_client" not in st.session_state:
        st.session_state.api_client = APIClient()
    return st.session_state.api_client