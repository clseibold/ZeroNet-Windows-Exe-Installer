#define MyAppName "ZeroNet"
#define MyAppVersion "1.0"
#define MyAppPublisher "ZeroNet"
#define MyAppURL "https://www.zeronet.io/"
#define MyAppExeName "ZeroNet.cmd"

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
Compression=lzma2
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Dirs]
Name: "{app}\ZeroNet\data"

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
Source: "ZeroBundle\ZeroNet.cmd"; DestDir: "{app}"; Flags: ignoreversion; \
  AfterInstall: SetElevationBit('{app}\{#MyAppExeName}')
Source: "ZeroBundle\*"; DestDir: "{app}"; Excludes: "\Python-x64\*,\ZeroNet\plugins\disabled-*\*,\ZeroNet\plugins\Trayicon\*"; Flags: ignoreversion recursesubdirs
;Source: "bin\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs
; Official Plugins
Source: "ZeroBundle\ZeroNet\plugins\Trayicon\*"; DestDir: "{app}\ZeroNet\plugins\Trayicon"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: officialplugins\trayicon
Source: "ZeroBundle\ZeroNet\plugins\disabled-UiPassword\*"; DestDir: "{app}\ZeroNet\plugins\UiPassword"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: officialplugins\uipassword
Source: "ZeroBundle\ZeroNet\plugins\disabled-Multiuser\*"; DestDir: "{app}\ZeroNet\plugins\Multiuser"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: officialplugins\multiuser
Source: "ZeroBundle\ZeroNet\plugins\disabled-Zeroname-local\*"; DestDir: "{app}\ZeroNet\plugins\Zeroname-local"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: officialplugins\zeronamelocal
; Third-Party Plugins
Source: "Plugins\P2P-messages\*"; DestDir: "{app}\ZeroNet\plugins\P2P-messages"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: thirdpartyplugins\p2pmessages

[Icons]
Name: "{group}\Data directory"; Filename: "{app}\ZeroNet\data"; Flags: foldershortcut
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\ZeroNet.ico"; \
  AfterInstall: SetElevationBit('{group}\{#MyAppName}.lnk')
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\ZeroNet.ico"; \
  AfterInstall: SetElevationBit('{commondesktop}\{#MyAppName}.lnk')

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Verb: runas; Flags: nowait postinstall skipifsilent shellexec

[Registry]
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers\"; \
  ValueType: String; ValueName: "{app}\{#MyAppExeName}"; ValueData: "RUNASADMIN"; \
  Flags: uninsdeletekeyifempty uninsdeletevalue; MinVersion: 0,6.1
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
	ValueType: String; ValueName: "ZERONET_ROOT"; ValueData: "{app}\ZeroNet"; Flags: uninsdeletekeyifempty uninsdeletevalue;
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
	ValueType: String; ValueName: "ZERONET_BUNDLE_ROOT"; ValueData: "{app}"; Flags: uninsdeletekeyifempty uninsdeletevalue;
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
	ValueType: String; ValueName: "ZERONET_DATA_DIR"; ValueData: "{app}\ZeroNet\data"; Flags: uninsdeletekeyifempty uninsdeletevalue;
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; \
    Check: NeedsAddPath(ExpandConstant('{app}'))

[InstallDelete]
; Delete files from old installation, version 1.2 and below
Type: files; Name: "{app}\gevent._semaphore.pyd"
Type: files; Name: "{app}\gevent.libev.corecext.pyd"
Type: files; Name: "{app}\Microsoft.VC90.CRT.manifest"
Type: files; Name: "{app}\msvcm90.dll"
Type: files; Name: "{app}\msvcp90.dll"
Type: files; Name: "{app}\msvcr90.dll"
Type: files; Name: "{app}\python27.dll"
; Notice
Type: files; Name: "{app}\ZeroNet.exe"
Type: files; Name: "{app}\ZeroNet.pkg"
Type: filesandordirs; Name: "{app}\bin"
Type: filesandordirs; Name: "{app}\log"
Type: filesandordirs; Name: "{app}\lib"
Type: filesandordirs; Name: "{app}\core"

[UninstallDelete]
Type: filesandordirs; Name: "{app}\ZeroNet\src"
Type: filesandordirs; Name: "{app}\Python"
	
[Code]
var
	DataDirMovePage: TInputDirWizardPage;

// Initialize wizard, add 'Move Data of Previous ZeroNet Instance' Page
procedure InitializeWizard;
begin
	DataDirMovePage := CreateInputDirPage(wpSelectDir,
		'Move Data of Previous ZeroNet Instance', 'Select a Data Directory to move to new ZeroNet installation',
		'Select the data folder of a previous ZeroNet instance that you want moved to the new ZeroNet installation, then click Next. If you do not want to move a data directory, then leave blank.',
		False, '');
	DataDirMovePage.Add('');
end;

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
	DelTree(ExpandConstant('{app}\ZeroNet\data'), True, True, True);
end;

// When page changed
procedure CurPageChanged(CurPageId: Integer);
begin
	if CurPageId = wpReady then
	begin
		if DataDirMovePage.Values[0] <> '' then
		begin
			Wizardform.ReadyMemo.Lines.Add('');
			Wizardform.ReadyMemo.Lines.Add('Move data directory to new ZeroNet installation');
			Wizardform.ReadyMemo.Lines.Add('    ' + DataDirMovePage.Values[0]);
		end;
	end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
		// Called after installation
	if CurStep = ssPostInstall then
	begin
		if DirExists(ExpandConstant('{app}\data')) and (DataDirMovePage.Values[0] = '') then begin
			Log('Moving data directory to new location');
			// Move data directory to new location
			if DirExists(ExpandConstant('{app}\ZeroNet\data')) then
			begin
				DelTree(ExpandConstant('{app}\ZeroNet\data'), True, True, True);
			end;
			RenameFile(ExpandConstant('{app}\data'), ExpandConstant('{app}\ZeroNet\data'));
		end;
		// Move old zeronet.conf file to new location
		if FileExists(ExpandConstant('{app}\zeronet.conf')) then begin
			Log('Moving zeronet.conf file to new location');
			if FileExists(ExpandConstant('{app}\ZeroNet\zeronet.conf')) then
			begin
				DeleteFile(ExpandConstant('{app}\ZeroNet\zeronet.conf'));
			end;
			RenameFile(ExpandConstant('{app}\zeronet.conf'), ExpandConstant('{app}\ZeroNet\zeronet.conf'));
		end;
		// Move the select data directory to the new location
		if (DataDirMovePage.Values[0] <> '') and DirExists(DataDirMovePage.Values[0]) then
		begin
			Log('Moving selected data directory.');
			if DirExists(ExpandConstant('{app}\ZeroNet\data')) then
			begin
				DelTree(ExpandConstant('{app}\ZeroNet\data'), True, True, True);
			end;
			RenameFile(DataDirMovePage.Values[0], ExpandConstant('{app}\ZeroNet\data'));
		end;
	end;
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