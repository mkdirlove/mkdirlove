@echo off
title KMS_VL_ALL 3.3.3
setlocal EnableExtensions
color 1f
:----------------------------------------
openfiles >nul 2>&1
if %errorlevel% NEQ 0 goto :UACPrompt
goto :gotAdmin
:UACPrompt
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
echo UAC.ShellExecute "%~fs0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs"
del "%temp%\getadmin.vbs"
exit /b
:gotAdmin
pushd "%~dp0"
:-----------------------------------------
::netsh advfirewall set allprofiles state off >nul 2>&1
::start /b cmd /c "KMS-HGM.exe" Port=1688 Office2010=Random Office2013=Random Windows=Random RenewalInterval=43200 ActivationInterval=43200 >nul 2>&1
call :SPP
call :OSPP
::taskkill /f /IM "KMS-HGM.exe" >nul 2>&1
::netsh advfirewall set allprofiles state on >nul 2>&1
echo.
echo.
echo Press any key to exit...
pause >nul
exit

:SPP
setlocal EnableDelayedExpansion
set spp=SoftwareLicensingProduct
set sps=SoftwareLicensingService
for /f "tokens=2 delims=[]" %%G in ('ver') do (for /f "tokens=2" %%G in ('echo %%G') do (set winnum=%%G))
if %winnum% LSS 6.2.9200 set /a win7=1
wmic path %spp% where (Description like '%%KMSCLIENT%%') get Name /format:list 2>nul | findstr /i Office >nul 2>&1
if %errorlevel% EQU 0 set /a office15=1
if %errorlevel% NEQ 0 (if defined win7 (echo.) else (echo.&echo No Supported KMS Client Office 2013 Detected...))
wmic path %spp% where (Description like '%%KMSCLIENT%%') get Name /format:list 2>nul | findstr /i Windows >nul 2>&1
if %errorlevel% EQU 0 set /a WinVL=1
if %errorlevel% NEQ 0 (echo.&echo No Supported KMS Client Windows Detected...)
if not defined office15 if not defined WinVL (endlocal&exit /b)
for /f "tokens=2 delims==" %%A in ('"wmic path %sps% get version /format:list"') do set ver=%%A
::for /f "tokens=2 delims==" %%A in ('"wmic path %sps% where version='%ver%' get KeyManagementServiceMachine /format:list" 2^>nul') do if not %%A==127.0.0.2 wmic path %sps% where version='%ver%' call SetKeyManagementServiceMachine MachineName="127.0.0.2" >nul 2>&1
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Description like '%%KMSCLIENT%%') get ID /format:list" 2^>nul') do call :sppchk %%A
::wmic path %sps% where version='%ver%' call ClearKeyManagementServiceMachine >nul 2>&1
::wmic path %sps% where version='%ver%' call ClearKeyManagementServiceListeningPort >nul 2>&1
::wmic path %sps% where version='%ver%' call DisableKeyManagementServiceDnsPublishing 1 >nul 2>&1
::wmic path %sps% where version='%ver%' call DisableKeyManagementServiceHostCaching 1 >nul 2>&1
endlocal
exit /b

:sppchk
set /a ls=0
set /a off15=0
for /f "tokens=2 delims==,,, " %%A in ('"wmic path %spp% where ID='%1' get Name /format:list"') do set name=%%A
if %name% EQU Office set /a off15=1
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where ID='%1' get LicenseStatus /format:list"') do set /a ls=%%A
if %ls% EQU 1 (call :activate %1&exit /b)
if %off15% EQU 1 (call :sppchkOffice15 %1) else (call :sppchkWindows %1)
exit /b

:sppchkWindows
wmic path %spp% where (Description like '%%VOLUME_MAK%%') get LicenseStatus /format:list 2>nul | findstr /i 1 >nul 2>&1
if %errorlevel% EQU 0 (echo.&echo Detected Windows is permanently activated.&exit /b)
wmic path %spp% where (Description like '%%OEM%%') get LicenseStatus /format:list 2>nul | findstr /i 1 >nul 2>&1
if %errorlevel% EQU 0 (echo.&echo Detected Windows is permanently activated.&exit /b)
wmic path %spp% where (Description like '%%System, RETAIL%%') get LicenseStatus /format:list 2>nul | findstr /i 1 >nul 2>&1
if %errorlevel% EQU 0 (echo.&echo Detected Windows is permanently activated.&exit /b)
wmic path %spp% where (Description like '%%7, RETAIL%%') get LicenseStatus /format:list 2>nul | findstr /i 1 >nul 2>&1
if %errorlevel% EQU 0 (echo.&echo Detected Windows is permanently activated.&exit /b)
call :insKey %1
call :activate %1
exit /b

:sppchkOffice15
set /a ls=0
if '%1' EQU 'b322da9c-a2e2-4058-9e4e-f59a6970bd69' (
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeProPlusVL_MAK%%') get LicenseStatus /format:list"') do set /a ls=%%A
if !ls! EQU 1 (echo.&echo Detected Office ProPlus 2013 is permanently activated.&exit /b) else (call :insKey %1&call :activate %1&exit /b)
)
if '%1' EQU 'b13afb38-cd79-4ae5-9f7f-eed058d750ca' (
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeStandardVL_MAK%%') get LicenseStatus /format:list"') do set /a ls=%%A
if !ls! EQU 1 (echo.&echo Detected Office Standard 2013 is permanently activated.&exit /b) else (call :insKey %1&call :activate %1&exit /b)
)
if '%1' EQU 'e13ac10e-75d0-4aff-a0cd-764982cf541c' (
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeVisioProVL_MAK%%') get LicenseStatus /format:list"') do set /a ls=%%A
if !ls! EQU 1 (echo.&echo Detected Visio Pro 2013 is permanently activated.&exit /b) else (call :insKey %1&call :activate %1&exit /b)
)
if '%1' EQU 'ac4efaf0-f81f-4f61-bdf7-ea32b02ab117' (
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeVisioStdVL_MAK%%') get LicenseStatus /format:list"') do set /a ls=%%A
if !ls! EQU 1 (echo.&echo Detected Visio Standard 2013 is permanently activated.&exit /b) else (call :insKey %1&call :activate %1&exit /b)
)
if '%1' EQU '4a5d124a-e620-44ba-b6ff-658961b33b9a' (
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeProjectProVL_MAK%%') get LicenseStatus /format:list"') do set /a ls=%%A
if !ls! EQU 1 (echo.&echo Detected Project Pro 2013 is permanently activated.&exit /b) else (call :insKey %1&call :activate %1&exit /b)
)
if '%1' EQU '427a28d1-d17c-4abf-b717-32c780ba6f07' (
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeProjectStdVL_MAK%%') get LicenseStatus /format:list"') do set /a ls=%%A
if !ls! EQU 1 (echo.&echo Detected Project Standard 2013 is permanently activated.&exit /b) else (call :insKey %1&call :activate %1&exit /b)
)

:OSPP
setlocal EnableDelayedExpansion
for /f "tokens=2 delims=[]" %%G in ('ver') do (for /f "tokens=2" %%G in ('echo %%G') do (set winnum=%%G))
if %winnum% LSS 6.2.9200 set /a win7=1
set spp=OfficeSoftwareProtectionProduct
set sps=OfficeSoftwareProtectionService
for /f "tokens=2 delims==" %%A in ('"wmic path %sps% get version /format:list" 2^>nul') do set ver=%%A
if not defined ver (if defined win7 (echo.&echo No Office 2010/2013 Product Detected...&endlocal&exit /b) else (echo.&echo No Office 2010 Product Detected...&endlocal&exit /b))
::for /f "tokens=2 delims==" %%A in ('"wmic path %sps% where version='%ver%' get KeyManagementServiceMachine /format:list"') do if not %%A==127.0.0.2 wmic path %sps% where version='%ver%' call SetKeyManagementServiceMachine MachineName="127.0.0.2" >nul 2>&1
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Description like '%%KMSCLIENT%%') get ID /format:list" 2^>nul') do call :osppchk %%A
::wmic path %sps% where version='%ver%' call ClearKeyManagementServiceMachine >nul 2>&1
::wmic path %sps% where version='%ver%' call ClearKeyManagementServiceListeningPort >nul 2>&1
::wmic path %sps% where version='%ver%' call DisableKeyManagementServiceDnsPublishing 1 >nul 2>&1
::wmic path %sps% where version='%ver%' call DisableKeyManagementServiceHostCaching 1 >nul 2>&1
endlocal
exit /b

:osppchk
set /a ls=0
set /a off14=0
if %ver% LSS 15 set /a off14=1
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where ID='%1' get LicenseStatus /format:list"') do set /a ls=%%A
if %ls% EQU 1 (call :activate %1&exit /b)
if %off14% EQU 1 (call :osppchkOffice14 %1) else (call :sppchkOffice15 %1)
exit /b

:osppchkOffice14
set /a ls=0
set /a ls2=0
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeVisioPrem-MAK%%') get LicenseStatus /format:list" 2^>nul') do set /a vPrem=%%A
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeVisioPro-MAK%%') get LicenseStatus /format:list" 2^>nul') do set /a vPro=%%A
if '%1' EQU 'df133ff7-bf14-4f95-afe3-7b48e7e331ef' (
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeProjectPro-MAK%%') get LicenseStatus /format:list"') do set /a ls=%%A
if !ls! EQU 1 (echo.&echo Detected Project Pro 2010 is permanently activated.&exit /b) else (call :insKey %1&call :activate %1&exit /b)
)
if '%1' EQU '5dc7bf61-5ec9-4996-9ccb-df806a2d0efe' (
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeProjectStd-MAK%%') get LicenseStatus /format:list"') do set /a ls=%%A
if !ls! EQU 1 (echo.&echo Detected Project Standard 2010 is permanently activated.&exit /b) else (call :insKey %1&call :activate %1&exit /b)
)
if '%1' EQU '6f327760-8c5c-417c-9b61-836a98287e0c' (
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeProPlus-MAK%%') get LicenseStatus /format:list"') do set /a ls=%%A
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeProPlusAcad-MAK%%') get LicenseStatus /format:list"') do set /a ls2=%%A
if !ls! EQU 1 (echo.&echo Detected Office ProPlus 2010 is permanently activated.&exit /b) 
if !ls2! EQU 1 (echo.&echo Detected Office ProPlus Academic 2010 is permanently activated.&exit /b) else (call :insKey %1&call :activate %1&exit /b)
)
if '%1' EQU '9da2a678-fb6b-4e67-ab84-60dd6a9c819a' (
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeStandard-MAK%%') get LicenseStatus /format:list"') do set /a ls=%%A
if !ls! EQU 1 (echo.&echo Detected Office Standard 2010 is permanently activated.&exit /b) else (call :insKey %1&call :activate %1&exit /b)
)
if '%1' EQU 'ea509e87-07a1-4a45-9edc-eba5a39f36af' (
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeSmallBusBasics-MAK%%') get LicenseStatus /format:list"') do set /a ls=%%A
if !ls! EQU 1 (echo.&echo Detected Office Small Business 2010 is permanently activated.&exit /b) else (call :insKey %1&call :activate %1&exit /b)
)
if '%1' EQU '92236105-bb67-494f-94c7-7f7a607929bd' (
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeVisioPrem-MAK%%') get LicenseStatus /format:list"') do set /a ls=%%A
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeVisioPro-MAK%%') get LicenseStatus /format:list"') do set /a ls2=%%A
if !ls! EQU 1 (echo.&echo Detected Visio Premium 2010 is permanently activated.&exit /b)
if !ls2! EQU 1 (echo.&echo Detected Visio Pro 2010 is permanently activated.&exit /b) else (call :insKey %1&call :activate %1&exit /b)
)
if defined vPrem exit /b
if '%1' EQU 'e558389c-83c3-4b29-adfe-5e4d7f46c358' (
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeVisioPro-MAK%%') get LicenseStatus /format:list"') do set /a ls=%%A
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeVisioStd-MAK%%') get LicenseStatus /format:list"') do set /a ls2=%%A
if !ls! EQU 1 (echo.&echo Detected Visio Pro 2010 is permanently activated.&exit /b)
if !ls2! EQU 1 (echo.&echo Detected Visio Standard 2010 is permanently activated.&exit /b) else (call :insKey %1&call :activate %1&exit /b)
)
if defined vPro exit /b
if '%1' EQU '9ed833ff-4f92-4f36-b370-8683a4f13275' (
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where (Name like '%%OfficeVisioStd-MAK%%') get LicenseStatus /format:list"') do set /a ls=%%A
if !ls! EQU 1 (echo.&echo Detected Visio Standard 2010 is permanently activated.&exit /b) else (call :insKey %1&call :activate %1&exit /b)
)

:activate
echo.
for /f "tokens=2 delims==" %%x in ('"wmic path %spp% where ID='%1' get Name /format:list"') do echo Attempting to activate %%x
set /p var=No. of Activation Attempts:  <nul
set /a retry=0
:act
wmic path %spp% where ID='%1' call Activate >nul 2>&1
set /a retry=%retry%+1
set /p var=%retry%<nul
for /f "tokens=2 delims==" %%x in ('"wmic path %spp% where ID='%1' get GracePeriodRemaining /format:list"') do set gpr=%%x
if %gpr% EQU 43200 (echo.&echo Remaining Period: 30 days&echo.&echo Windows 8 Core/WMC Activation Successful&exit /b)
if %gpr% LSS 259200 if %retry% LSS 3 goto act
set /a gpr=%gpr%/60/24
echo.
echo Remaining Period: %gpr% day(s)
echo.
if %gpr% EQU 180 ( set msg=Product Activation Successful
echo.&echo !msg!
) else ( set msg=Product Activation Failed
echo.&echo !msg!
)
exit /b

:insKey
echo.
for /f "tokens=2 delims==" %%A in ('"wmic path %spp% where ID='%1' get Name /format:list"') do echo Installing Key for %%A
set file="%~dp0key.vbs"
echo edition = "%1">%file%
echo Set keys = CreateObject ("Scripting.Dictionary")>>%file%
echo keys.Add "aa6dd3aa-c2b4-40e2-a544-a6bbb3f5c395", "73KQT-CD9G6-K7TQG-66MRP-CQ22C">>%file%
echo keys.Add "db537896-376f-48ae-a492-53d0547773d0", "YBYF6-BHCR3-JPKRB-CDW7B-F9BK4">>%file%
echo keys.Add "6f327760-8c5c-417c-9b61-836a98287e0c", "VYBBJ-TRJPB-QFQRF-QFT4D-H3GVB">>%file%
echo keys.Add "9da2a678-fb6b-4e67-ab84-60dd6a9c819a", "V7QKV-4XVVR-XYV4D-F7DFM-8R6BM">>%file%
echo keys.Add "ea509e87-07a1-4a45-9edc-eba5a39f36af", "D6QFG-VBYP2-XQHM7-J97RH-VVRCK">>%file%
echo keys.Add "8ce7e872-188c-4b98-9d90-f8f90b7aad02", "V7Y44-9T38C-R2VJK-666HK-T7DDX">>%file%
echo keys.Add "cee5d470-6e3b-4fcc-8c2b-d17428568a9f", "H62QG-HXVKF-PP4HP-66KMR-CW9BM">>%file%
echo keys.Add "8947d0b8-c33b-43e1-8c56-9b674c052832", "QYYW6-QP4CB-MBV6G-HYMCJ-4T3J4">>%file%
echo keys.Add "ca6b6639-4ad6-40ae-a575-14dee07f6430", "K96W8-67RPQ-62T9Y-J8FQJ-BT37T">>%file%
echo keys.Add "ab586f5c-5256-4632-962f-fefd8b49e6f4", "Q4Y4M-RHWJM-PY37F-MTKWH-D3XHX">>%file%
echo keys.Add "ecb7c192-73ab-4ded-acf4-2399b095d0cc", "7YDC2-CWM8M-RRTJC-8MDVC-X3DWQ">>%file%
echo keys.Add "45593b1d-dfb1-4e91-bbfb-2d5d0ce2227a", "RC8FX-88JRY-3PF7C-X8P67-P4VTT">>%file%
echo keys.Add "df133ff7-bf14-4f95-afe3-7b48e7e331ef", "YGX6F-PGV49-PGW3J-9BTGG-VHKC6">>%file%
echo keys.Add "5dc7bf61-5ec9-4996-9ccb-df806a2d0efe", "4HP3K-88W3F-W2K3D-6677X-F9PGB">>%file%
echo keys.Add "b50c4f75-599b-43e8-8dcd-1081a7967241", "BFK7F-9MYHM-V68C7-DRQ66-83YTP">>%file%
echo keys.Add "2d0882e7-a4e7-423b-8ccc-70d91e0158b1", "HVHB3-C6FV7-KQX9W-YQG79-CRY7T">>%file%
echo keys.Add "92236105-bb67-494f-94c7-7f7a607929bd", "D9DWC-HPYVV-JGF4P-BTWQB-WX8BJ">>%file%
echo keys.Add "e558389c-83c3-4b29-adfe-5e4d7f46c358", "7MCW8-VRQVK-G677T-PDJCM-Q8TCP">>%file%
echo keys.Add "9ed833ff-4f92-4f36-b370-8683a4f13275", "767HD-QGMWX-8QTDB-9G3R2-KHFGJ">>%file%
echo keys.Add "09ed9640-f020-400a-acd8-d7d867dfd9c2", "YBJTT-JG6MD-V9Q7P-DBKXJ-38W9R">>%file%
echo keys.Add "ef3d4e49-a53d-4d81-a2b1-2ca6c2556b2c", "7TC2V-WXF6P-TD7RT-BQRXR-B8K32">>%file%
echo keys.Add "ae2ee509-1b34-41c0-acb7-6d4650168915", "33PXH-7Y6KF-2VJC9-XBBR8-HVTHH">>%file%
echo keys.Add "46bbed08-9c7b-48fc-a614-95250573f4ea", "C29WB-22CC8-VJ326-GHFJW-H9DH4">>%file%
echo keys.Add "1cb6d605-11b3-4e14-bb30-da91c8e3983a", "YDRBP-3D83W-TY26F-D46B2-XCKRJ">>%file%
echo keys.Add "b92e9980-b9d5-4821-9c94-140f632f6312", "FJ82H-XT6CR-J8D7P-XQJJ2-GPDD4">>%file%
echo keys.Add "5a041529-fef8-4d07-b06f-b59b573b32d2", "W82YF-2Q76Y-63HXB-FGJG9-GF7QX">>%file%
echo keys.Add "54a09a0d-d57b-4c10-8b69-a842d6590ad5", "MRPKT-YTG23-K7D7T-X2JMM-QY7MG">>%file%
echo keys.Add "7482e61b-c589-4b7f-8ecc-46d455ac3b87", "74YFP-3QFB3-KQT8W-PMXWJ-7M648">>%file%
echo keys.Add "620e2b3d-09e7-42fd-802a-17a13652fe7a", "489J6-VHDMP-X63PK-3K798-CPX3Y">>%file%
echo keys.Add "8a26851c-1c7e-48d3-a687-fbca9b9ac16b", "GT63C-RJFQ3-4GMB6-BRFB9-CB83V">>%file%
echo keys.Add "f772515c-0e87-48d5-a676-e6962c3e1195", "736RG-XDKJK-V34PF-BHK87-J6X3K">>%file%
echo keys.Add "cda18cf3-c196-46ad-b289-60c072869994", "TT8MH-CG224-D3D7Q-498W2-9QCTX">>%file%
echo keys.Add "68531fb9-5511-4989-97be-d11a0f55633f", "YC6KT-GKW9T-YTKYR-T4X34-R7VHC">>%file%
echo keys.Add "a78b8bd9-8017-4df5-b86a-09f756affa7c", "6TPJF-RBVHG-WBW2R-86QPH-6RTM4">>%file%
echo keys.Add "4f3d1606-3fea-4c01-be3c-8d671c401e3b", "YFKBB-PQJJV-G996G-VWGXY-2V3X8">>%file%
echo keys.Add "2c682dc2-8b68-4f63-a165-ae291d4cf138", "HMBQG-8H2RH-C77VX-27R82-VMQBT">>%file%
echo keys.Add "cfd8ff08-c0d7-452b-9f60-ef5c70c32094", "VKK3X-68KWM-X2YGT-QR4M6-4BWMV">>%file%
echo keys.Add "d4f54950-26f2-4fb4-ba21-ffab16afcade", "VTC42-BM838-43QHV-84HX6-XJXKV">>%file%
echo keys.Add "7afb1156-2c1d-40fc-b260-aab7442b62fe", "RCTX3-KWVHP-BR6TB-RB6DM-6X7HP">>%file%
echo keys.Add "68b6e220-cf09-466b-92d3-45cd964b9509", "7M67G-PC374-GR742-YH8V4-TCBY3">>%file%
echo keys.Add "fd09ef77-5647-4eff-809c-af2b64659a45", "22XQ2-VRXRG-P8D42-K34TD-G3QQC">>%file%
echo keys.Add "c1af4d90-d1bc-44ca-85d4-003ba33db3b9", "YQGMW-MPWTJ-34KDK-48M3W-X4Q6V">>%file%
echo keys.Add "8198490a-add0-47b2-b3ba-316b12d647b4", "39BXF-X8Q23-P2WWT-38T2F-G3FPG">>%file%
echo keys.Add "01ef176b-3e0d-422a-b4f8-4ea880035e8f", "4DWFP-JF3DJ-B7DTH-78FJB-PDRHK">>%file%
echo keys.Add "ad2542d4-9154-4c6d-8a44-30f11ee96989", "TM24T-X9RMF-VWXK6-X8JC9-BFGM2">>%file%
echo keys.Add "2401e3d0-c50a-4b58-87b2-7e794b7d2607", "W7VD6-7JFBR-RX26B-YKQ3Y-6FFFJ">>%file%
echo keys.Add "ddfa9f7c-f09e-40b9-8c1a-be877a9a7f4b", "WYR28-R7TFJ-3X2YQ-YCY4H-M249D">>%file%
echo keys.Add "b322da9c-a2e2-4058-9e4e-f59a6970bd69", "YC7DK-G2NP3-2QQC3-J6H88-GVGXT">>%file%
echo keys.Add "b13afb38-cd79-4ae5-9f7f-eed058d750ca", "KBKQT-2NMXY-JJWGP-M62JB-92CD4">>%file%
echo keys.Add "4a5d124a-e620-44ba-b6ff-658961b33b9a", "FN8TT-7WMH6-2D4X9-M337T-2342K">>%file%
echo keys.Add "427a28d1-d17c-4abf-b717-32c780ba6f07", "6NTH3-CW976-3G3Y2-JK3TX-8QHTT">>%file%
echo keys.Add "e13ac10e-75d0-4aff-a0cd-764982cf541c", "C2FG9-N6J68-H8BTJ-BW3QX-RM3B3">>%file%
echo keys.Add "ac4efaf0-f81f-4f61-bdf7-ea32b02ab117", "J484Y-4NKBF-W2HMG-DBMJC-PGWR7">>%file%
echo keys.Add "6ee7622c-18d8-4005-9fb7-92db644a279b", "NG2JY-H4JBT-HQXYP-78QH9-4JM2D">>%file%
echo keys.Add "f7461d52-7c2b-43b2-8744-ea958e0bd09a", "VGPNG-Y7HQW-9RHP7-TKPV3-BG7GB">>%file%
echo keys.Add "a30b8040-d68a-423f-b0b5-9ce292ea5a8f", "DKT8B-N7VXH-D963P-Q4PHY-F8894">>%file%
echo keys.Add "1b9f11e3-c85c-4e1b-bb29-879ad2c909e3", "2MG3G-3BNTT-3MFW9-KDQW3-TCK7R">>%file%
echo keys.Add "efe1f3e6-aea2-4144-a208-32aa872b6545", "TGN6P-8MMBC-37P2F-XHXXK-P34VW">>%file%
echo keys.Add "771c3afa-50c5-443f-b151-ff2546d863a0", "QPN8Q-BJBTJ-334K3-93TGY-2PMBT">>%file%
echo keys.Add "8c762649-97d1-4953-ad27-b7e2c25b972e", "4NT99-8RJFH-Q2VDH-KYG2C-4RD4F">>%file%
echo keys.Add "00c79ff1-6850-443d-bf61-71cde0de305f", "PN2WF-29XG2-T9HJ7-JQPJR-FCXK4">>%file%
echo keys.Add "d9f5b1c6-5386-495a-88f9-9ad6b41ac9b3", "6Q7VD-NX8JD-WJ2VH-88V73-4GBJ7">>%file%
echo keys.Add "a98bcd6d-5343-4603-8afe-5908e4611112", "NG4HW-VH26C-733KW-K6F98-J8CK4">>%file%
echo keys.Add "ebf245c1-29a8-4daf-9cb1-38dfc608a8c8", "XCVCF-2NXM9-723PB-MHCB7-2RYQQ">>%file%
echo keys.Add "a00018a3-f20f-4632-bf7c-8daa5351c914", "GNBB8-YVD74-QJHX6-27H4K-8QHDG">>%file%
echo keys.Add "458e1bec-837a-45f6-b9d5-925ed5d299de", "32JNW-9KQ84-P47T8-D8GGY-CWCK7">>%file%
echo keys.Add "e14997e7-800a-4cf7-ad10-de4b45b578db", "JMNMF-RHW7P-DMY6X-RF3DR-X2BQT">>%file%
echo keys.Add "c04ed6bf-55c8-4b47-9f8e-5a1f31ceee60", "BN3D2-R7TKB-3YPBD-8DRP2-27GG4">>%file%
echo keys.Add "197390a0-65f6-4a95-bdc4-55d58a3b0253", "8N2M2-HWPGY-7PGT9-HGDD8-GVGGY">>%file%
echo keys.Add "8860fcd4-a77b-4a20-9045-a150ff11d609", "2WN2H-YGCQR-KFX6K-CD6TF-84YXQ">>%file%
echo keys.Add "9d5584a2-2d85-419a-982c-a00888bb9ddf", "4K36P-JN4VD-GDC6V-KDT89-DYFKP">>%file%
echo keys.Add "f0f5ec41-0d55-4732-af02-440a44a3cf0f", "XC9B7-NBPP2-83J2H-RHMBY-92BT4">>%file%
echo keys.Add "7d5486c7-e120-4771-b7f1-7b56c6d3170c", "HM7DN-YVMH3-46JC3-XYTG7-CYQJJ">>%file%
echo keys.Add "95fd1c83-7df5-494a-be8b-1300e1c9d1cd", "XNH6W-2V9GX-RGJ4K-Y8X6F-QGJ2G">>%file%
echo keys.Add "d3643d60-0c42-412d-a7d6-52e6635327f6", "48HP8-DN98B-MYWDG-T2DCC-8W83P">>%file%
echo if keys.Exists(edition) then>>%file%
echo WScript.Echo keys.Item(edition)>>%file%
echo End If>>%file%
for /f %%A in ('cscript /nologo %file%') do set key=%%A
del %file%
wmic path %sps% where version='%ver%' call InstallProductKey ProductKey="%key%" >nul 2>&1
exit /b