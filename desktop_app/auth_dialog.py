"""
Login/Signup Window for Chemical Equipment Visualizer
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTabWidget, QWidget,
    QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QFont
from api_client import APIClient
from config import COLORS


class AuthDialog(QDialog):
    """Authentication dialog for login/signup"""
    
    authenticated = pyqtSignal(str, str)  # Emits (access_token, refresh_token)
    
    def __init__(self, api_client: APIClient, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("Chemical Equipment Visualizer - Login")
        self.setFixedSize(450, 550)
        self.setModal(True)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)
        
        # Logo/Title Section
        title_frame = QFrame()
        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)
        
        # Icon (using Unicode character as placeholder)
        icon_label = QLabel("🧪")
        icon_label.setStyleSheet(f"font-size: 48px;")
        icon_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(icon_label)
        
        title = QLabel("Chemical Equipment\nParameter Visualizer")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['primary']}; font-size: 20px; font-weight: bold;")
        title_layout.addWidget(title)
        
        subtitle = QLabel("AI-Powered Analysis Platform")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        title_layout.addWidget(subtitle)
        
        title_frame.setLayout(title_layout)
        layout.addWidget(title_frame)
        
        # Tab Widget for Login/Signup
        self.tab_widget = QTabWidget()
        
        # Login Tab
        login_tab = QWidget()
        login_layout = QVBoxLayout()
        login_layout.setSpacing(15)
        
        login_layout.addWidget(QLabel("Username"))
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        login_layout.addWidget(self.login_username)
        
        login_layout.addWidget(QLabel("Password"))
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.returnPressed.connect(self.handle_login)
        login_layout.addWidget(self.login_password)
        
        self.login_button = QPushButton("Sign In")
        self.login_button.clicked.connect(self.handle_login)
        login_layout.addWidget(self.login_button)
        
        login_layout.addStretch()
        login_tab.setLayout(login_layout)
        
        # Signup Tab
        signup_tab = QWidget()
        signup_layout = QVBoxLayout()
        signup_layout.setSpacing(15)
        
        signup_layout.addWidget(QLabel("Username"))
        self.signup_username = QLineEdit()
        self.signup_username.setPlaceholderText("Choose a username")
        signup_layout.addWidget(self.signup_username)
        
        signup_layout.addWidget(QLabel("Email"))
        self.signup_email = QLineEdit()
        self.signup_email.setPlaceholderText("Enter your email")
        signup_layout.addWidget(self.signup_email)
        
        signup_layout.addWidget(QLabel("Password"))
        self.signup_password = QLineEdit()
        self.signup_password.setEchoMode(QLineEdit.Password)
        self.signup_password.setPlaceholderText("Choose a password")
        self.signup_password.returnPressed.connect(self.handle_signup)
        signup_layout.addWidget(self.signup_password)
        
        self.signup_button = QPushButton("Sign Up")
        self.signup_button.clicked.connect(self.handle_signup)
        signup_layout.addWidget(self.signup_button)
        
        signup_layout.addStretch()
        signup_tab.setLayout(signup_layout)
        
        # Add tabs
        self.tab_widget.addTab(login_tab, "Login")
        self.tab_widget.addTab(signup_tab, "Sign Up")
        
        layout.addWidget(self.tab_widget)
        
        self.setLayout(layout)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        try:
            self.login_button.setEnabled(False)
            self.login_button.setText("Signing in...")
            
            # Attempt login
            response = self.api_client.login(username, password)
            
            # Emit success signal
            self.authenticated.emit(
                self.api_client.access_token,
                self.api_client.refresh_token
            )
            
            self.accept()
            
        except Exception as e:
            error_msg = str(e)
            if '401' in error_msg:
                QMessageBox.critical(self, "Login Failed", "Invalid username or password")
            elif 'Network' in error_msg or 'Connection' in error_msg:
                QMessageBox.critical(self, "Connection Error", 
                                   "Cannot connect to server. Please check if the backend is running.")
            else:
                QMessageBox.critical(self, "Login Failed", f"Error: {error_msg}")
        finally:
            self.login_button.setEnabled(True)
            self.login_button.setText("Sign In")
    
    def handle_signup(self):
        """Handle signup button click"""
        username = self.signup_username.text().strip()
        email = self.signup_email.text().strip()
        password = self.signup_password.text()
        
        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        
        if '@' not in email:
            QMessageBox.warning(self, "Error", "Please enter a valid email address")
            return
        
        try:
            self.signup_button.setEnabled(False)
            self.signup_button.setText("Creating account...")
            
            # Attempt signup
            response = self.api_client.signup(username, email, password)
            
            # Emit success signal
            self.authenticated.emit(
                self.api_client.access_token,
                self.api_client.refresh_token
            )
            
            QMessageBox.information(self, "Success", "Account created successfully!")
            self.accept()
            
        except Exception as e:
            error_msg = str(e)
            if '400' in error_msg:
                QMessageBox.critical(self, "Signup Failed", 
                                   "Username or email already exists")
            elif 'Network' in error_msg or 'Connection' in error_msg:
                QMessageBox.critical(self, "Connection Error", 
                                   "Cannot connect to server. Please check if the backend is running.")
            else:
                QMessageBox.critical(self, "Signup Failed", f"Error: {error_msg}")
        finally:
            self.signup_button.setEnabled(True)
            self.signup_button.setText("Sign Up")
