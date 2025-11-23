"""
Chemical Equipment Parameter Visualizer - Desktop Application
Main entry point
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from api_client import APIClient
from auth_dialog import AuthDialog
from main_window import MainWindow
from config import STYLESHEET


def main():
    """Main application entry point"""
    # Enable high DPI scaling (must be set before QApplication)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create application
    app = QApplication(sys.argv)
    
    # Set application-wide stylesheet
    app.setStyleSheet(STYLESHEET)
    
    # Create API client
    api_client = APIClient()
    
    # Show login dialog
    auth_dialog = AuthDialog(api_client)
    
    if auth_dialog.exec_() == auth_dialog.Accepted:
        # User logged in successfully
        main_window = MainWindow(api_client)
        main_window.show()
        
        # Run application
        sys.exit(app.exec_())
    else:
        # User cancelled login
        sys.exit(0)


if __name__ == '__main__':
    main()
