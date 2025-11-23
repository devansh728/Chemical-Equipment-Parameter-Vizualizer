"""
Main Window for Chemical Equipment Visualizer Desktop App
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QTableWidget, QTableWidgetItem,
    QListWidget, QListWidgetItem, QMessageBox, QTabWidget,
    QTextEdit, QFrame, QSplitter, QProgressDialog, QHeaderView,
    QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor
import os
from datetime import datetime
from api_client import APIClient
from config import COLORS, APP_NAME


class UploadWorker(QThread):
    """Background worker for file upload"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_client, file_path):
        super().__init__()
        self.api_client = api_client
        self.file_path = file_path
    
    def run(self):
        try:
            result = self.api_client.upload_csv(self.file_path)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class DataFetchWorker(QThread):
    """Background worker for fetching dataset details"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_client, dataset_id):
        super().__init__()
        self.api_client = api_client
        self.dataset_id = dataset_id
    
    def run(self):
        try:
            details = self.api_client.get_dataset_detail(self.dataset_id)
            stats = self.api_client.get_dataset_stats(self.dataset_id)
            details['stats'] = stats
            self.finished.emit(details)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        self.current_dataset_id = None
        self.current_dataset_details = None
        
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 1400, 900)
        
        self.init_ui()
        self.load_history()
        
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh_current_dataset)
        self.refresh_timer.start(10000)  # Refresh every 10 seconds
    
    def init_ui(self):
        """Initialize the user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Content splitter (history sidebar + main content)
        splitter = QSplitter(Qt.Horizontal)
        
        # Left sidebar - History
        sidebar = self.create_sidebar()
        splitter.addWidget(sidebar)
        
        # Right content - Tabs
        self.content_tabs = self.create_content_tabs()
        splitter.addWidget(self.content_tabs)
        
        # Set splitter sizes (30% sidebar, 70% content)
        splitter.setSizes([350, 1050])
        
        main_layout.addWidget(splitter)
        
        central_widget.setLayout(main_layout)
    
    def create_header(self) -> QWidget:
        """Create header with title and upload button"""
        header = QFrame()
        header.setFrameShape(QFrame.NoFrame)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 10)
        
        # Title
        title_layout = QVBoxLayout()
        title = QLabel(APP_NAME)
        title.setStyleSheet(f"color: {COLORS['primary']}; font-size: 28px; font-weight: bold;")
        title_layout.addWidget(title)
        
        subtitle = QLabel("AI-Powered Chemical Equipment Analysis")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Upload button
        self.upload_button = QPushButton("📁 Upload CSV")
        self.upload_button.setFixedHeight(45)
        self.upload_button.clicked.connect(self.upload_file)
        header_layout.addWidget(self.upload_button)
        
        # Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.setObjectName("secondaryButton")
        self.logout_button.setFixedHeight(45)
        self.logout_button.clicked.connect(self.logout)
        header_layout.addWidget(self.logout_button)
        
        header.setLayout(header_layout)
        return header
    
    def create_sidebar(self) -> QWidget:
        """Create sidebar with dataset history"""
        sidebar = QFrame()
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(10)
        
        # Title
        history_label = QLabel("📊 Recent Datasets")
        history_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLORS['text_primary']};")
        sidebar_layout.addWidget(history_label)
        
        # History list
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.on_dataset_selected)
        sidebar_layout.addWidget(self.history_list)
        
        # Refresh button
        refresh_button = QPushButton("🔄 Refresh History")
        refresh_button.setObjectName("secondaryButton")
        refresh_button.clicked.connect(self.load_history)
        sidebar_layout.addWidget(refresh_button)
        
        sidebar.setLayout(sidebar_layout)
        return sidebar
    
    def create_content_tabs(self) -> QTabWidget:
        """Create main content tabs"""
        tabs = QTabWidget()
        
        # Overview Tab
        self.overview_tab = self.create_overview_tab()
        tabs.addTab(self.overview_tab, "📈 Overview")
        
        # Statistics Tab
        self.stats_tab = self.create_stats_tab()
        tabs.addTab(self.stats_tab, "📊 Statistics")
        
        # AI Insights Tab
        self.ai_tab = self.create_ai_tab()
        tabs.addTab(self.ai_tab, "🤖 AI Insights")
        
        # Data Table Tab
        self.data_tab = self.create_data_tab()
        tabs.addTab(self.data_tab, "📋 Data")
        
        return tabs
    
    def create_overview_tab(self) -> QWidget:
        """Create overview tab with stats cards"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Welcome message
        self.overview_welcome = QLabel("Select a dataset from history or upload a new CSV file")
        self.overview_welcome.setStyleSheet(f"font-size: 16px; color: {COLORS['text_secondary']}; padding: 40px;")
        self.overview_welcome.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.overview_welcome)
        
        # Stats cards (hidden initially)
        self.stats_cards = QWidget()
        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)
        
        # Create stat cards
        self.total_records_card = self.create_stat_card("Total Records", "0", "📊")
        self.avg_pressure_card = self.create_stat_card("Avg Pressure", "0.0 PSI", "⚙️")
        self.avg_temp_card = self.create_stat_card("Avg Temperature", "0.0°F", "🌡️")
        self.status_card = self.create_stat_card("Status", "N/A", "✅")
        
        stats_layout.addWidget(self.total_records_card, 0, 0)
        stats_layout.addWidget(self.avg_pressure_card, 0, 1)
        stats_layout.addWidget(self.avg_temp_card, 1, 0)
        stats_layout.addWidget(self.status_card, 1, 1)
        
        self.stats_cards.setLayout(stats_layout)
        self.stats_cards.hide()
        layout.addWidget(self.stats_cards)
        
        # Download report button
        self.download_report_button = QPushButton("📄 Download PDF Report")
        self.download_report_button.setFixedHeight(45)
        self.download_report_button.clicked.connect(self.download_report)
        self.download_report_button.hide()
        layout.addWidget(self.download_report_button)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_stat_card(self, title: str, value: str, icon: str) -> QFrame:
        """Create a statistics card"""
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border-radius: 12px;
                border: 2px solid {COLORS['border']};
                padding: 20px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        # Icon and title
        header_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 13px; color: {COLORS['text_secondary']};")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName(f"{title.lower().replace(' ', '_')}_value")
        value_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {COLORS['primary']};")
        layout.addWidget(value_label)
        
        card.setLayout(layout)
        card.value_label = value_label  # Store reference for updates
        return card
    
    def create_stats_tab(self) -> QWidget:
        """Create statistics tab with detailed stats table"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("Detailed Statistical Summary")
        label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {COLORS['primary']};")
        layout.addWidget(label)
        
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(8)
        self.stats_table.setHorizontalHeaderLabels([
            "Parameter", "Mean", "Median", "Std Dev", "Min", "Q1", "Q3", "Max"
        ])
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.stats_table)
        
        widget.setLayout(layout)
        return widget
    
    def create_ai_tab(self) -> QWidget:
        """Create AI insights tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("🤖 AI-Generated Insights")
        label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {COLORS['primary']};")
        layout.addWidget(label)
        
        self.ai_insights_text = QTextEdit()
        self.ai_insights_text.setReadOnly(True)
        self.ai_insights_text.setPlaceholderText("AI insights will appear here after analysis completes...")
        layout.addWidget(self.ai_insights_text)
        
        # Suggestions section
        suggestions_label = QLabel("💡 Smart Suggestions")
        suggestions_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLORS['primary']}; margin-top: 15px;")
        layout.addWidget(suggestions_label)
        
        self.ai_suggestions_text = QTextEdit()
        self.ai_suggestions_text.setReadOnly(True)
        self.ai_suggestions_text.setPlaceholderText("AI suggestions will appear here...")
        self.ai_suggestions_text.setMaximumHeight(200)
        layout.addWidget(self.ai_suggestions_text)
        
        widget.setLayout(layout)
        return widget
    
    def create_data_tab(self) -> QWidget:
        """Create data table tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("Dataset Preview")
        label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {COLORS['primary']};")
        layout.addWidget(label)
        
        self.data_table = QTableWidget()
        layout.addWidget(self.data_table)
        
        widget.setLayout(layout)
        return widget
    
    def upload_file(self):
        """Handle file upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )
        
        if file_path:
            progress = QProgressDialog("Uploading file...", None, 0, 0, self)
            progress.setWindowModality(Qt.WindowModal)
            progress.show()
            
            self.upload_worker = UploadWorker(self.api_client, file_path)
            self.upload_worker.finished.connect(lambda result: self.on_upload_finished(result, progress))
            self.upload_worker.error.connect(lambda error: self.on_upload_error(error, progress))
            self.upload_worker.start()
    
    def on_upload_finished(self, result, progress):
        """Handle successful upload"""
        progress.close()
        QMessageBox.information(self, "Success", 
                              f"File uploaded successfully!\nProcessing started...")
        self.load_history()
    
    def on_upload_error(self, error, progress):
        """Handle upload error"""
        progress.close()
        QMessageBox.critical(self, "Upload Failed", f"Error: {error}")
    
    def load_history(self):
        """Load dataset history"""
        try:
            history = self.api_client.get_history()
            self.history_list.clear()
            
            for dataset in history:
                item = QListWidgetItem()
                
                # Format display text
                filename = dataset.get('filename', f"Dataset #{dataset['id']}")
                date = datetime.fromisoformat(dataset['uploaded_at'].replace('Z', '+00:00'))
                date_str = date.strftime('%m/%d %H:%M')
                status = dataset.get('status', 'UNKNOWN')
                records = dataset.get('total_records', 0)
                
                # Status emoji
                status_emoji = {
                    'COMPLETED': '✅',
                    'PROCESSING': '⏳',
                    'PROFILING': '🔍',
                    'ANALYZING': '📊',
                    'AI_PROCESSING': '🤖',
                    'FAILED': '❌'
                }.get(status, '⚪')
                
                text = f"{status_emoji} {filename}\n{date_str} • {records} records • {status}"
                item.setText(text)
                item.setData(Qt.UserRole, dataset['id'])
                
                self.history_list.addItem(item)
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load history: {e}")
    
    def on_dataset_selected(self, item):
        """Handle dataset selection"""
        dataset_id = item.data(Qt.UserRole)
        self.current_dataset_id = dataset_id
        
        progress = QProgressDialog("Loading dataset...", None, 0, 0, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        
        self.data_worker = DataFetchWorker(self.api_client, dataset_id)
        self.data_worker.finished.connect(lambda details: self.on_dataset_loaded(details, progress))
        self.data_worker.error.connect(lambda error: self.on_dataset_error(error, progress))
        self.data_worker.start()
    
    def on_dataset_loaded(self, details, progress):
        """Handle dataset loaded"""
        progress.close()
        self.current_dataset_details = details
        self.update_ui_with_dataset(details)
    
    def on_dataset_error(self, error, progress):
        """Handle dataset load error"""
        progress.close()
        QMessageBox.warning(self, "Error", f"Failed to load dataset: {error}")
    
    def update_ui_with_dataset(self, details):
        """Update UI with dataset details"""
        # Update overview tab
        self.overview_welcome.hide()
        self.stats_cards.show()
        self.download_report_button.show()
        
        # Update stat cards
        stats = details.get('stats', {})
        self.total_records_card.value_label.setText(str(stats.get('total_records', 0)))
        self.avg_pressure_card.value_label.setText(f"{stats.get('avg_pressure', 0):.1f} PSI")
        self.avg_temp_card.value_label.setText(f"{stats.get('avg_temperature', 0):.1f}°F")
        self.status_card.value_label.setText(details.get('status', 'UNKNOWN'))
        
        # Update statistics table
        enhanced_summary = details.get('enhanced_summary', {})
        numeric_cols = enhanced_summary.get('numeric_columns', {})
        
        self.stats_table.setRowCount(len(numeric_cols))
        for i, (col_name, col_stats) in enumerate(numeric_cols.items()):
            self.stats_table.setItem(i, 0, QTableWidgetItem(col_name))
            self.stats_table.setItem(i, 1, QTableWidgetItem(f"{col_stats.get('mean', 0):.2f}"))
            self.stats_table.setItem(i, 2, QTableWidgetItem(f"{col_stats.get('median', 0):.2f}"))
            self.stats_table.setItem(i, 3, QTableWidgetItem(f"{col_stats.get('std', 0):.2f}"))
            self.stats_table.setItem(i, 4, QTableWidgetItem(f"{col_stats.get('min', 0):.2f}"))
            self.stats_table.setItem(i, 5, QTableWidgetItem(f"{col_stats.get('q1', 0):.2f}"))
            self.stats_table.setItem(i, 6, QTableWidgetItem(f"{col_stats.get('q3', 0):.2f}"))
            self.stats_table.setItem(i, 7, QTableWidgetItem(f"{col_stats.get('max', 0):.2f}"))
        
        # Update AI insights
        ai_insights = details.get('ai_insights', {})
        if ai_insights:
            insights_text = ai_insights.get('executive_summary', 'No insights available')
            self.ai_insights_text.setPlainText(insights_text)
        
        ai_suggestions = details.get('ai_suggestions', {})
        if ai_suggestions:
            suggestions = ai_suggestions.get('suggestions', [])
            # Handle both string list and dict list formats
            if suggestions:
                if isinstance(suggestions[0], dict):
                    # Dict format: {'suggestion': '...', 'reasoning': '...'}
                    suggestions_text = "\n\n".join([
                        f"💡 {s.get('suggestion', 'N/A')}\n   → {s.get('reasoning', '')}"
                        for s in suggestions
                    ])
                else:
                    # String list format
                    suggestions_text = "\n\n".join(suggestions)
                self.ai_suggestions_text.setPlainText(suggestions_text)
            else:
                self.ai_suggestions_text.setPlaceholderText("No suggestions available yet...")
        
        # Update data table
        data = details.get('data', [])
        if data:
            self.data_table.setRowCount(len(data))
            self.data_table.setColumnCount(len(data[0]))
            self.data_table.setHorizontalHeaderLabels(list(data[0].keys()))
            
            for i, row in enumerate(data):
                for j, (key, value) in enumerate(row.items()):
                    self.data_table.setItem(i, j, QTableWidgetItem(str(value)))
            
            self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def auto_refresh_current_dataset(self):
        """Auto-refresh current dataset if processing"""
        if self.current_dataset_id and self.current_dataset_details:
            status = self.current_dataset_details.get('status', '')
            if status in ['PROCESSING', 'PROFILING', 'ANALYZING', 'AI_PROCESSING']:
                # Silently refresh
                try:
                    details = self.api_client.get_dataset_detail(self.current_dataset_id)
                    stats = self.api_client.get_dataset_stats(self.current_dataset_id)
                    details['stats'] = stats
                    self.current_dataset_details = details
                    self.update_ui_with_dataset(details)
                except:
                    pass
    
    def download_report(self):
        """Download PDF report"""
        if not self.current_dataset_id:
            return
        
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            f"report_{self.current_dataset_id}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if save_path:
            try:
                progress = QProgressDialog("Downloading report...", None, 0, 0, self)
                progress.setWindowModality(Qt.WindowModal)
                progress.show()
                
                self.api_client.download_report(self.current_dataset_id, save_path)
                
                progress.close()
                QMessageBox.information(self, "Success", f"Report saved to:\n{save_path}")
            except Exception as e:
                progress.close()
                QMessageBox.critical(self, "Error", f"Failed to download report: {e}")
    
    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(self, "Logout", 
                                    "Are you sure you want to logout?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.api_client.logout()
            self.close()
