﻿#define MyAppName "Battle Observer"
#define MyAppPublisher "Armagomen, Inc."
#define MyAppURL "https://github.com/Armagomen/battle_observer"
#define MyAppUpdatesURL MyAppURL+"/releases/latest/"
#define WOT_VERSION_PATTERN "1.*"
#define APP_FILE_PATTERN "mod_battle_observer_v"
#define APP_DIR_UNINST "battle_observer_uninst"
#define OPENWGUTILS_DIR_SRC    "dll"
#define OPENWGUTILS_DIR_UNINST APP_DIR_UNINST

#include "scripts\openwg.utils.iss"
#include "scripts\code.iss"

#ifndef MyAppVersion
  #define MyAppVersion "0.0.0.0"
#endif

[Setup]
AppId={{E4911938-A29D-4904-8878-99DEEBDE03D6}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
VersionInfoVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL=https://discord.gg/Nma5T5snKW
AppUpdatesURL={#MyAppUpdatesURL}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=..\..\
OutputBaseFilename={#APP_FILE_PATTERN}{#MyAppVersion}
DefaultDirName=C:\
SetupIconFile=img\game.ico
WizardStyle=modern
DirExistsWarning=no
CreateAppDir=yes
AppendDefaultDirName=no
ShowLanguageDialog=yes
Uninstallable=yes
UsePreviousAppDir=yes

UninstallFilesDir={app}\{#APP_DIR_UNINST}

[Run]
Filename: "https://donatua.com/to/armagomen"; Description: "{cm:open_donate}"; Flags: postinstall nowait shellexec;

[InstallDelete]
Type: files; Name: "{app}\{code:PH_Folder_Mods}\armagomen.battleObserver*.wotmod"
Type: files; Name: "{app}\{code:PH_Folder_Mods}\me.poliroid.modslistapi*.wotmod"
Type: files; Name: "{app}\{code:PH_Folder_Mods}\polarfox.vxSettingsApi*.wotmod"
Type: filesandordirs; Name: "{app}\mods\configs\mod_battle_observer\armagomen\*.*"

[UninstallDelete]
Type: files; Name: "{app}\{code:PH_Folder_Mods}\armagomen.battleObserver*.wotmod"

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"; LicenseFile: "..\EULA_EN.txt"; 
Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"; LicenseFile: "..\EULA_EN.txt";
Name: "uk"; MessagesFile: "compiler:Languages\Ukrainian.isl"; LicenseFile: "..\EULA_UK.txt";

[Icons]
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

#include "scripts\messages.iss"
#include "scripts\components.iss"
