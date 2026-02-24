# app/ui/update_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QTextEdit
)
from PySide6.QtCore import Qt, QThread, Signal
from app.updater import download_installer, launch_installer_and_exit


class DownloadThread(QThread):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            path = download_installer(self.url, self.progress.emit)
            self.finished.emit(path)
        except Exception as e:
            self.error.emit(str(e))


class UpdateDialog(QDialog):
    def __init__(self, update_info: dict, parent=None):
        super().__init__(parent)
        self.update_info = update_info
        self.installer_path = None
        self.setWindowTitle("Update Available")
        self.setMinimumWidth(420)
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Title
        title = QLabel(f"🎉 Version {self.update_info['version']} is available!")
        title.setStyleSheet("font-size: 15px; font-weight: bold;")
        layout.addWidget(title)

        # Release notes
        notes_label = QLabel("What's new:")
        layout.addWidget(notes_label)

        notes = QTextEdit()
        notes.setReadOnly(True)
        notes.setPlainText(self.update_info.get("release_notes", "No notes provided."))
        notes.setMaximumHeight(100)
        layout.addWidget(notes)

        # Progress bar (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Buttons
        btn_layout = QHBoxLayout()

        self.download_btn = QPushButton("Download & Install")
        self.download_btn.setStyleSheet("background-color: #0078d4; color: white; padding: 6px 16px;")
        self.download_btn.clicked.connect(self._start_download)

        skip_btn = QPushButton("Skip")
        skip_btn.clicked.connect(self.reject)

        btn_layout.addWidget(skip_btn)
        btn_layout.addWidget(self.download_btn)
        layout.addLayout(btn_layout)

    def _start_download(self):
        self.download_btn.setEnabled(False)
        self.download_btn.setText("Downloading...")
        self.progress_bar.setVisible(True)
        self.status_label.setText("Downloading update...")

        self.thread = DownloadThread(self.update_info["download_url"])
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.finished.connect(self._on_download_done)
        self.thread.error.connect(self._on_download_error)
        self.thread.start()

    def _on_download_done(self, path):
        self.installer_path = path
        self.status_label.setText("Download complete! Launching installer...")
        launch_installer_and_exit(path)

    def _on_download_error(self, error):
        self.status_label.setText(f"Error: {error}")
        self.download_btn.setEnabled(True)
        self.download_btn.setText("Retry")