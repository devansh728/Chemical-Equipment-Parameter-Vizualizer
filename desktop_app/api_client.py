"""
API Client for Chemical Equipment Visualizer Desktop App
Handles all communication with the Django backend
"""
import requests
from typing import Optional, Dict, Any, List
from config import API_BASE_URL


class APIClient:
    """Client for interacting with the backend API"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.session = requests.Session()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token"""
        headers = {'Content-Type': 'application/json'}
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        return headers
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user and store tokens
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            Dict with user info and tokens
            
        Raises:
            requests.HTTPError: If authentication fails
        """
        response = self.session.post(
            f'{self.base_url}/api/token/',
            json={'username': username, 'password': password}
        )
        response.raise_for_status()
        
        data = response.json()
        self.access_token = data['access']
        self.refresh_token = data['refresh']
        
        return data
    
    def signup(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """
        Register new user
        
        Args:
            username: Desired username
            email: User's email
            password: Desired password
            
        Returns:
            Dict with user info and tokens
            
        Raises:
            requests.HTTPError: If signup fails
        """
        response = self.session.post(
            f'{self.base_url}/api/signup/',
            json={'username': username, 'email': email, 'password': password}
        )
        response.raise_for_status()
        
        data = response.json()
        self.access_token = data['tokens']['access']
        self.refresh_token = data['tokens']['refresh']
        
        return data
    
    def refresh_access_token(self) -> str:
        """
        Refresh the access token using refresh token
        
        Returns:
            New access token
            
        Raises:
            requests.HTTPError: If refresh fails
        """
        if not self.refresh_token:
            raise ValueError("No refresh token available")
        
        response = self.session.post(
            f'{self.base_url}/api/token/refresh/',
            json={'refresh': self.refresh_token}
        )
        response.raise_for_status()
        
        data = response.json()
        self.access_token = data['access']
        return self.access_token
    
    def upload_csv(self, file_path: str) -> Dict[str, Any]:
        """
        Upload CSV file for analysis
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Dict with upload response
            
        Raises:
            requests.HTTPError: If upload fails
        """
        headers = {}
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = self.session.post(
                f'{self.base_url}/api/upload/',
                files=files,
                headers=headers
            )
        
        response.raise_for_status()
        return response.json()
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get list of uploaded datasets
        
        Returns:
            List of dataset summaries
            
        Raises:
            requests.HTTPError: If request fails
        """
        response = self.session.get(
            f'{self.base_url}/api/history/',
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_dataset_detail(self, dataset_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a dataset
        
        Args:
            dataset_id: ID of the dataset
            
        Returns:
            Dict with dataset details
            
        Raises:
            requests.HTTPError: If request fails
        """
        response = self.session.get(
            f'{self.base_url}/api/dataset/{dataset_id}/',
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_dataset_stats(self, dataset_id: int) -> Dict[str, Any]:
        """
        Get statistical summary for a dataset
        
        Args:
            dataset_id: ID of the dataset
            
        Returns:
            Dict with stats (total_records, avg_pressure, etc.)
            
        Raises:
            requests.HTTPError: If request fails
        """
        response = self.session.get(
            f'{self.base_url}/api/dataset/{dataset_id}/stats/',
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_correlations(self, dataset_id: int) -> Dict[str, Any]:
        """
        Get correlation matrix for a dataset
        
        Args:
            dataset_id: ID of the dataset
            
        Returns:
            Dict with correlation data
            
        Raises:
            requests.HTTPError: If request fails
        """
        response = self.session.get(
            f'{self.base_url}/api/dataset/{dataset_id}/correlation/',
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_optimizations(self, dataset_id: int) -> Dict[str, Any]:
        """
        Get optimization recommendations for a dataset
        
        Args:
            dataset_id: ID of the dataset
            
        Returns:
            Dict with optimization recommendations
            
        Raises:
            requests.HTTPError: If request fails
        """
        response = self.session.get(
            f'{self.base_url}/api/dataset/{dataset_id}/optimize/',
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def explain_outlier(self, dataset_id: int, outlier_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get AI explanation for an outlier
        
        Args:
            dataset_id: ID of the dataset
            outlier_data: Dict with outlier information
            
        Returns:
            Dict with explanation
            
        Raises:
            requests.HTTPError: If request fails
        """
        response = self.session.post(
            f'{self.base_url}/api/dataset/{dataset_id}/explain-outlier/',
            json=outlier_data,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def download_report(self, dataset_id: int, save_path: str) -> None:
        """
        Download PDF report for a dataset
        
        Args:
            dataset_id: ID of the dataset
            save_path: Path to save the PDF file
            
        Raises:
            requests.HTTPError: If download fails
        """
        response = self.session.get(
            f'{self.base_url}/api/dataset/{dataset_id}/report/',
            headers=self._get_headers(),
            stream=True
        )
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    
    def logout(self) -> None:
        """Clear authentication tokens"""
        self.access_token = None
        self.refresh_token = None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.access_token is not None
