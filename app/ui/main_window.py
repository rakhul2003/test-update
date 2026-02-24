# app/ui/main_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QHBoxLayout, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from app.updater import check_for_updates, get_current_version
from app.ui.update_dialog import UpdateDialog


class UpdateCheckThread(QThread):
    result = Signal(object)  # dict or None

    def run(self):
        self.result.emit(check_for_updates())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Update App - Print Defect Detector")
        self.setMinimumSize(500, 350)
        self._build_ui()
        self._auto_check_updates()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(16)
        layout.setContentsMargins(30, 30, 30, 30)

        # App title
        title = QLabel("🖨️ Print Defect Detector")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        # Current version
        self.version_label = QLabel(f"Current Version: v{get_current_version()}")
        self.version_label.setStyleSheet("color: gray; font-size: 13px;")
        layout.addWidget(self.version_label)

        # Fake app content
        content = QLabel("✅ App is running normally.\nThis is v1.0.0 - Basic UI")
        content.setStyleSheet("font-size: 14px; margin-top: 20px;")
        layout.addWidget(content)

        layout.addStretch()

        # Bottom bar: auto update toggle + check button
        bottom = QHBoxLayout()

        self.auto_update_checkbox = QCheckBox("Auto-check updates on startup")
        self.auto_update_checkbox.setChecked(True)
        bottom.addWidget(self.auto_update_checkbox)

        bottom.addStretch()

        check_btn = QPushButton("🔄 Check for Updates")
        check_btn.clicked.connect(self._manual_check_updates)
        bottom.addWidget(check_btn)

        layout.addLayout(bottom)

        # Status bar
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: gray; font-size: 11px;")
        self.statusBar().addWidget(self.status_label)

    def _auto_check_updates(self):
        if self.auto_update_checkbox.isChecked():
            self.status_label.setText("Checking for updates...")
            self.thread = UpdateCheckThread()
            self.thread.result.connect(self._on_update_check_result)
            self.thread.start()

    def _manual_check_updates(self):
        self.status_label.setText("Checking for updates...")
        self.thread = UpdateCheckThread()
        self.thread.result.connect(lambda result: self._on_update_check_result(result, manual=True))
        self.thread.start()

    def _on_update_check_result(self, update_info, manual=False):
        if update_info:
            self.status_label.setText(f"Update available: v{update_info['version']}")
            dialog = UpdateDialog(update_info, parent=self)
            dialog.exec()
        else:
            self.status_label.setText("You are up to date ✓")
            if manual:
                QMessageBox.information(self, "No Updates", "You already have the latest version!")