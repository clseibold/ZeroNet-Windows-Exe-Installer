#define MyAppName "ZeroNet"
#define MyAppVersion "1.0"
#define MyAppPublisher "ZeroNet"
#define MyAppURL "https://www.zeronet.io/"
#define MyAppExeName "ZeroNet.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{7C632D38-8512-4141-9AAE-C61BB83AE099}
PrivilegesRequired=admin
; Tell Windows Explorer to reload the environment
ChangesEnvironment=yes
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputBaseFilename=ZeroNetInstaller
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Dirs]
Name: "{app}\bin"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
;Name: "p2pmessagesplugin"; Description: "P2P Messages"; GroupDescription: "Install Additional Plugins"

[Types]
Name: "full"; Description: "Full client installation"
Name: "minimal"; Description: "Minimal client installation"
Name: "fullserver"; Description: "Full proxy server installation"
Name: "minimalserver"; Description: "Minimal proxy server installation"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "main"; Description: "Base install"; Types: full minimal fullserver minimalserver custom; Flags: fixed
; Official Plugins
Name: "officialplugins"; Description: "Official Plugins"; Types: full fullserver custom
Name: "officialplugins\trayicon"; Description: "Tray icon"; Types: full minimal fullserver
Name: "officialplugins\uipassword"; Description: "UiPassword"; Types: fullserver
Name: "officialplugins\multiuser"; Description: "Multiuser"; Types: fullserver
Name: "officialplugins\zeronamelocal"; Description: "ZeroName Local"
; Third-Party Plugins
Name: "thirdpartyplugins"; Description: "Third-Party Plugins"; Types: full fullserver custom
Name: "thirdpartyplugins\p2pmessages"; Description: "P2P Messages Plugin (imachug) - Beta"; Types: full fullserver

[Files]
; NOTE: Don't use "Flags: ignoreversion" on any shared system files
; Base Install
Source: "ZeroNet-win-dist\ZeroNet.exe"; DestDir: "{app}"; Flags: ignoreversion; \
  AfterInstall: SetElevationBit('{app}\{#MyAppExeName}')
Source: "ZeroNet-win-dist\*"; DestDir: "{app}"; Excludes: "\core\plugins\disabled-*\*,\core\plugins\Trayicon\*"; Flags: ignoreversion recursesubdirs
Source: "bin\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs
; Official Plugins
Source: "ZeroNet-win-dist\core\plugins\Trayicon\*"; DestDir: "{app}\core\plugins\Trayicon"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: officialplugins\trayicon
Source: "ZeroNet-win-dist\core\plugins\disabled-UiPassword\*"; DestDir: "{app}\core\plugins\UiPassword"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: officialplugins\uipassword
Source: "ZeroNet-win-dist\core\plugins\disabled-Multiuser\*"; DestDir: "{app}\core\plugins\Multiuser"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: officialplugins\multiuser
Source: "ZeroNet-win-dist\core\plugins\disabled-Zeroname-local\*"; DestDir: "{app}\core\plugins\Zeroname-local"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: officialplugins\zeronamelocal
; Third-Party Plugins
Source: "Plugins\P2P-messages\*"; DestDir: "{app}\core\plugins\P2P-messages"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: thirdpartyplugins\p2pmessages

[Icons]
Name: "{group}\Data directory"; Filename: "{app}\data"; Flags: foldershortcut
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; \
  AfterInstall: SetElevationBit('{group}\{#MyAppName}.lnk')
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; \
  AfterInstall: SetElevationBit('{commondesktop}\{#MyAppName}.lnk')

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Verb: runas; Flags: nowait postinstall skipifsilent shellexec

[Registry]
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers\"; \
  ValueType: String; ValueName: "{app}\{#MyAppExeName}"; ValueData: "RUNASADMIN"; \
  Flags: uninsdeletekeyifempty uninsdeletevalue; MinVersion: 0,6.1
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
	ValueType: String; ValueName: "ZERONET_ROOT"; ValueData: "{app}\core"; Flags: uninsdeletekeyifempty uninsdeletevalue;
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
	ValueType: String; ValueName: "ZERONET_BUNDLE_ROOT"; ValueData: "{app}"; Flags: uninsdeletekeyifempty uninsdeletevalue;
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
	ValueType: String; ValueName: "ZERONET_DATA_DIR"; ValueData: "{app}\data"; Flags: uninsdeletekeyifempty uninsdeletevalue;
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
	ValueType: String; ValueName: "ZERONET_DATA_DIR"; ValueData: "{app}\data"; Flags: uninsdeletekeyifempty uninsdeletevalue;
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}\bin"; \
    Check: NeedsAddPath(ExpandConstant('{app}\bin'))

[UninstallDelete]
Type: filesandordirs; Name: "{app}\core"
Type: filesandordirs; Name: "{app}\lib"
	
[Code]
procedure SetElevationBit(Filename: string);
var
  Buffer: string;
  Stream: TStream;
begin
  Filename := ExpandConstant(Filename);
  Log('Setting elevation bit for ' + Filename);

  Stream := TFileStream.Create(FileName, fmOpenReadWrite);
  try
    Stream.Seek(21, soFromBeginning);
    SetLength(Buffer, 1);
    Stream.ReadBuffer(Buffer, 1);
    Buffer[1] := Chr(Ord(Buffer[1]) or $20);
    Stream.Seek(-1, soFromCurrent);
    Stream.WriteBuffer(Buffer, 1);
  finally
    Stream.Free;
  end;
end;

// Used to add bin directory to global PATH only if not already in it
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  { look for the path with leading and trailing semicolon }
  { Pos() returns 0 if not found }
  Result :=
    (Pos(';' + UpperCase(Param) + ';', ';' + UpperCase(OrigPath) + ';') = 0) and
    (Pos(';' + UpperCase(Param) + '\;', ';' + UpperCase(OrigPath) + ';') = 0); 
end;

// Delete ZeroNet Data Directory Procedure
procedure DeleteDataDirectory();
begin
	DelTree(ExpandConstant('{app}\data'), True, True, True);
end;

// Called after uninstallation
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then begin
    if MsgBox('Do you want to delete the ZeroNet data folder?', mbConfirmation,
        MB_YESNO) = IDYES 
    then begin
      DeleteDataDirectory();
    end;
  end;
end;