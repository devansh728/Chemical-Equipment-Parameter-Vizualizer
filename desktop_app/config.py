"""
Configuration module for Chemical Equipment Visualizer Desktop App
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')
WS_BASE_URL = os.getenv('WS_BASE_URL', 'ws://localhost:8000')

# Application Settings
APP_NAME = "Chemical Equipment Visualizer"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# Theme Colors (Material Design inspired)
COLORS = {
    'primary': '#6366f1',
    'primary_dark': '#4f46e5',
    'primary_light': '#818cf8',
    'accent': '#f59e0b',
    'background': '#f8fafc',
    'surface': '#ffffff',
    'text_primary': '#1e293b',
    'text_secondary': '#64748b',
    'border': '#e2e8f0',
    'success': '#10b981',
    'error': '#ef4444',
    'warning': '#f59e0b',
    'info': '#3b82f6'
}

# Styles
STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS['background']};
}}

QWidget {{
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    color: {COLORS['text_primary']};
}}

QPushButton {{
    background-color: {COLORS['primary']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 600;
    min-width: 100px;
}}

QPushButton:hover {{
    background-color: {COLORS['primary_dark']};
}}

QPushButton:pressed {{
    background-color: {COLORS['primary_light']};
}}

QPushButton:disabled {{
    background-color: #cbd5e1;
    color: #94a3b8;
}}

QPushButton#secondaryButton {{
    background-color: {COLORS['surface']};
    color: {COLORS['primary']};
    border: 2px solid {COLORS['primary']};
}}

QPushButton#secondaryButton:hover {{
    background-color: {COLORS['primary_light']};
    color: white;
}}

QPushButton#dangerButton {{
    background-color: {COLORS['error']};
}}

QPushButton#dangerButton:hover {{
    background-color: #dc2626;
}}

QLineEdit, QTextEdit {{
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    padding: 10px;
    background-color: {COLORS['surface']};
}}

QLineEdit:focus, QTextEdit:focus {{
    border: 2px solid {COLORS['primary']};
}}

QLabel {{
    color: {COLORS['text_primary']};
}}

QLabel#titleLabel {{
    font-size: 24px;
    font-weight: bold;
    color: {COLORS['primary']};
}}

QLabel#subtitleLabel {{
    font-size: 14px;
    color: {COLORS['text_secondary']};
}}

QFrame {{
    background-color: {COLORS['surface']};
    border-radius: 12px;
    border: 1px solid {COLORS['border']};
}}

QTableWidget {{
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    background-color: {COLORS['surface']};
    gridline-color: {COLORS['border']};
}}

QTableWidget::item {{
    padding: 8px;
}}

QTableWidget::item:selected {{
    background-color: {COLORS['primary_light']};
    color: white;
}}

QHeaderView::section {{
    background-color: {COLORS['primary']};
    color: white;
    padding: 10px;
    border: none;
    font-weight: 600;
}}

QListWidget {{
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    background-color: {COLORS['surface']};
}}

QListWidget::item {{
    padding: 12px;
    border-bottom: 1px solid {COLORS['border']};
}}

QListWidget::item:selected {{
    background-color: {COLORS['primary_light']};
    color: white;
}}

QListWidget::item:hover {{
    background-color: #f1f5f9;
}}

QProgressBar {{
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    text-align: center;
    background-color: {COLORS['surface']};
}}

QProgressBar::chunk {{
    background-color: {COLORS['primary']};
    border-radius: 4px;
}}

QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    background-color: {COLORS['surface']};
}}

QTabBar::tab {{
    background-color: {COLORS['background']};
    color: {COLORS['text_secondary']};
    padding: 10px 20px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 4px;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['primary']};
    color: white;
}}

QTabBar::tab:hover {{
    background-color: {COLORS['primary_light']};
    color: white;
}}

QScrollBar:vertical {{
    border: none;
    background-color: {COLORS['background']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['text_secondary']};
}}

QScrollBar:horizontal {{
    border: none;
    background-color: {COLORS['background']};
    height: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {COLORS['text_secondary']};
}}

QMenuBar {{
    background-color: {COLORS['surface']};
    border-bottom: 1px solid {COLORS['border']};
}}

QMenuBar::item {{
    padding: 8px 12px;
}}

QMenuBar::item:selected {{
    background-color: {COLORS['primary_light']};
    color: white;
}}

QMenu {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
}}

QMenu::item {{
    padding: 8px 24px;
}}

QMenu::item:selected {{
    background-color: {COLORS['primary_light']};
    color: white;
}}
"""
