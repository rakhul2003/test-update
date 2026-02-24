[Setup]
AppName=PrintDefectDetector
AppVersion=2.0.0
DefaultDirName={autopf}\PrintDefectDetector
DefaultGroupName=PrintDefectDetector
OutputDir=R:\Documents\RDX\test-update\test-update\dist\installer
OutputBaseFilename=PrintDefectDetectorSetup_v2.0.0
Compression=lzma
SolidCompression=yes

[Files]
Source: "R:\Documents\RDX\test-update\test-update\dist\PrintDefectDetector\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\PrintDefectDetector"; Filename: "{app}\PrintDefectDetector.exe"
Name: "{commondesktop}\PrintDefectDetector"; Filename: "{app}\PrintDefectDetector.exe"

[Run]
Filename: "{app}\PrintDefectDetector.exe"; Description: "Launch app"; Flags: nowait postinstall skipifsilent
```

Save it → go back to Inno Setup → press **`Ctrl + F9`**

You should see **"Successfully compiled"** and the installer will be created at:
```
R:\Documents\RDX\test-update\test-update\dist\installer\PrintDefectDetectorSetup_v2.0.0.exe