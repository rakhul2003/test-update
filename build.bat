@echo off
echo Building PrintDefectDetector...

REM Build exe
uv run pyinstaller --windowed --onedir --name "PrintDefectDetector" app/main.py

echo Done! Now open installer/setup.iss in Inno Setup to create the installer.
pause
```

---

## 🚀 Full Workflow Summary
```
V1 RELEASE:
─────────────────────────────────────────────────────
1. Code is version "1.0.0" in updater.py and pyproject.toml
2. Run: build.bat  → creates dist/PrintDefectDetector/
3. Open Inno Setup → open installer/setup.iss → click Build
4. Upload PrintDefectDetectorSetup_v1.0.0.exe to GitHub Releases
5. Push version.json with version: "1.0.0" to GitHub repo
6. Share installer with customer ✅

V2 RELEASE (new feature / bug fix):
─────────────────────────────────────────────────────
1. Change CURRENT_VERSION = "2.0.0" in updater.py
2. Update content label in main_window.py to show "v2.0.0"
3. Run build.bat again
4. Open Inno Setup → change AppVersion to 2.0.0 → Build
5. Upload PrintDefectDetectorSetup_v2.0.0.exe to GitHub Releases
6. Update version.json → version: "2.0.0", new download_url, new release_notes
7. Push version.json → customers get notified automatically ✅