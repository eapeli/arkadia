; Damon Agent NSIS Custom Installer Script
; This script customizes the NSIS installer for Windows

!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "WinCore.nsh"
!include "LogicLib.nsh"

; ----------------------------------------------------------------
; Basic Configuration
; ----------------------------------------------------------------
Name "Damon Agent"
OutFile "Damon-Setup-${PRODUCT_VERSION}-${ARCH}.exe"
InstallDir "$PROGRAMFILES64\Damon Agent"
InstallDirRegKey HKLM "Software\Damon Agent" "Install_Dir"
RequestExecutionLevel admin
ShowInstDetails show

; ----------------------------------------------------------------
; UI Configuration
; ----------------------------------------------------------------
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"
!define MUI_WELCOMEFINISHPAGE_BITMAP "icons/nsis-welcome.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "icons/nsis-welcome.bmp"
!define MUI_INSTFILESPAGE_COLORS 000000 FFFFFF
!define MUI_UNINSTFILESPAGE_COLORS 000000 FFFFFF

; Custom Pages
!define MUI_PAGE_CUSTOMFUNCTION_PRE WelcomePage
!define MUI_PAGE_CUSTOMFUNCTION_PRE DirectoryPage
!define MUI_PAGE_CUSTOMFUNCTION_PRE InstFilesPage
!define MUI_UNPAGE_CUSTOMFUNCTION_PRE UninstWelcomePage
!define MUI_UNPAGE_CUSTOMFUNCTION_PRE UninstConfirmPage

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.md"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages - Portuguese first (default), then English
!insertmacro MUI_LANGUAGE "Portuguese"
!insertmacro MUI_LANGUAGE "English"

; ----------------------------------------------------------------
; Variables
; ----------------------------------------------------------------
Var /GLOBAL PreviousInstallDir
Var /GLOBAL InstallType
Var /GLOBAL RunAfterInstall
Var /GLOBAL SelectedLanguage

; ----------------------------------------------------------------
; Language Strings
; ----------------------------------------------------------------

; Portuguese (default)
LangString DESC_SecMain ${LANG_PORTUGUESE} "Aplicação Principal"
LangString DESC_SecShortcuts ${LANG_PORTUGUESE} "Atalhos do Menu Iniciar"
LangString DESC_SecDesktop ${LANG_PORTUGUESE} "Atalho na Área de Trabalho"
LangString MSG_UpgradeFound ${LANG_PORTUGUESE} "Uma versão anterior do Damon Agent foi encontrada em:\n$PreviousInstallDir\n\nDeseja atualizá-la?"
LangString MSG_AdminRequired ${LANG_PORTUGUESE} "Este instalador requer privilégios de administrador."
LangString MSG_InstallSuccess ${LANG_PORTUGUESE} "O Damon Agent foi instalado com sucesso!\n\nExecute 'damon' em qualquer terminal para começar."

; English
LangString DESC_SecMain ${LANG_ENGLISH} "Main Application"
LangString DESC_SecShortcuts ${LANG_ENGLISH} "Start Menu Shortcuts"
LangString DESC_SecDesktop ${LANG_ENGLISH} "Desktop Shortcut"
LangString MSG_UpgradeFound ${LANG_ENGLISH} "A previous version of Damon Agent was found at:\n$PreviousInstallDir\n\nDo you want to upgrade it?"
LangString MSG_AdminRequired ${LANG_ENGLISH} "This installer requires administrator privileges."
LangString MSG_InstallSuccess ${LANG_ENGLISH} "Damon Agent has been installed successfully!\n\nRun 'damon' from any terminal to get started."

; ----------------------------------------------------------------
; Functions
; ----------------------------------------------------------------

Function WelcomePage
    ; Check for previous installation
    ReadRegStr $PreviousInstallDir HKLM "Software\Damon Agent" "Install_Dir"
    ${If} $PreviousInstallDir != ""
        ${If} ${FileExists} "$PreviousInstallDir\damon.exe"
            MessageBox MB_YESNO "$(MSG_UpgradeFound)" IDYES NoUpgrade
            StrCpy $InstallDir $PreviousInstallDir
        NoUpgrade:
        ${EndIf}
    ${EndIf}
FunctionEnd

Function DirectoryPage
    ; Store selected directory
    StrCpy $PreviousInstallDir $InstallDir
FunctionEnd

Function InstFilesPage
    ; Pre-install tasks
FunctionEnd

Function UninstWelcomePage
FunctionEnd

Function UninstConfirmPage
FunctionEnd

; ----------------------------------------------------------------
; Sections
; ----------------------------------------------------------------

Section "$(DESC_SecMain)" SecMain
    SectionIn RO

    ; Set output path
    SetOutPath "$InstallDir"

    ; Copy application files
    File /r "..\dist\*"

    ; Copy install scripts
    File /r "..\..\..\scripts\install.ps1"
    File /r "..\..\..\scripts\install.sh"

    ; Create uninstaller
    WriteUninstaller "$InstallDir\uninstall.exe"

    ; Registry entries
    WriteRegStr HKLM "Software\Damon Agent" "Install_Dir" "$InstallDir"
    WriteRegStr HKLM "Software\Damon Agent" "Version" "${PRODUCT_VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DamonAgent" "DisplayName" "Damon Agent"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DamonAgent" "UninstallString" "$InstallDir\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DamonAgent" "DisplayVersion" "${PRODUCT_VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DamonAgent" "Publisher" "Damon Agent Team"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DamonAgent" "URLInfoAbout" "https://damon-agent.dev"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DamonAgent" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DamonAgent" "NoRepair" 1

    ; Add to PATH (system-wide)
    ${GetParameters} $0
    ${EnvVar::SetValue} "PATH" "$InstallDir" "1" "HKLM"

    ; Create shortcuts
    CreateDirectory "$SMPROGRAMS\Damon Agent"
    CreateShortcut "$SMPROGRAMS\Damon Agent\Damon Agent.lnk" "$InstallDir\damon.exe"
    CreateShortcut "$SMPROGRAMS\Damon Agent\Uninstall.lnk" "$InstallDir\uninstall.exe"
    ${If} ${RunningX64}
        CreateShortcut "$DESKTOP\Damon Agent.lnk" "$InstallDir\damon.exe"
    ${EndIf}

SectionEnd

Section "$(DESC_SecShortcuts)" SecShortcuts
    SectionIn 1
    CreateDirectory "$SMPROGRAMS\Damon Agent"
    CreateShortcut "$SMPROGRAMS\Damon Agent\Damon Agent.lnk" "$InstallDir\damon.exe"
    CreateShortcut "$SMPROGRAMS\Damon Agent\Uninstall.lnk" "$InstallDir\uninstall.exe"
    CreateShortcut "$SMPROGRAMS\Damon Agent\Documentation.url" "https://damon-agent.dev/docs"
SectionEnd

Section "$(DESC_SecDesktop)" SecDesktop
    SectionIn 1
    CreateShortcut "$DESKTOP\Damon Agent.lnk" "$InstallDir\damon.exe"
SectionEnd

; ----------------------------------------------------------------
; Uninstaller
; ----------------------------------------------------------------

Section Uninstall
    ; Remove from PATH
    ${EnvVar::DeleteValue} "PATH" "$InstallDir" "HKLM"

    ; Remove registry
    DeleteRegKey HKLM "Software\Damon Agent"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DamonAgent"

    ; Remove shortcuts
    Delete "$SMPROGRAMS\Damon Agent\*.*"
    RMDir "$SMPROGRAMS\Damon Agent"
    Delete "$DESKTOP\Damon Agent.lnk"

    ; Remove files
    RMDir /r "$InstallDir"
SectionEnd

; ----------------------------------------------------------------
; Custom Functions
; ----------------------------------------------------------------

Function .onInit
    ; Check for admin rights
    UserInfo::GetAccountType
    Pop $0
    StrCmp $0 "Admin" +3
    MessageBox MB_ICONSTOP "This installer requires administrator privileges."
    Abort

    ; Initialize
    InitPluginsDir
FunctionEnd

Function .onInstSuccess
    ; Run post-install script if requested
    ${If} $RunAfterInstall == 1
        ExecWait '"$InstallDir\install.ps1" -NonInteractive'
    ${EndIf}

    ; Show completion message
    MessageBox MB_OK "$(MSG_InstallSuccess)"
FunctionEnd

Function .onUninstSuccess
    ; Clean up
    HideWindow
FunctionEnd