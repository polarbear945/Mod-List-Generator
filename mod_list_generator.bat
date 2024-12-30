@echo off
setlocal
echo Downloading open_links.bat
powershell -Command "Invoke-WebRequest -Uri https://github.com/polarbear945/Mod-List-Generator/raw/refs/heads/main/open_links.bat -OutFile open_links.bat"
echo Downloading uninstall_generator.bat
powershell -Command "Invoke-WebRequest -Uri https://github.com/polarbear945/Mod-List-Generator/raw/refs/heads/main/uninstall_generator.bat -OutFile uninstall_generator.bat"
mkdir files
cd files
echo Downloading generate_csv.py
powershell -Command "Invoke-WebRequest -Uri https://github.com/polarbear945/Mod-List-Generator/raw/refs/heads/main/files/generate_csv.py -OutFile generate_csv.py"
echo Downloading open_links.py
powershell -Command "Invoke-WebRequest -Uri https://github.com/polarbear945/Mod-List-Generator/raw/refs/heads/main/files/open_links.py -OutFile open_links.py"
echo Downloading version_query.py
powershell -Command "Invoke-WebRequest -Uri https://github.com/polarbear945/Mod-List-Generator/raw/refs/heads/main/files/version_query.py -OutFile version_query.py"
cd ..
echo Creating a virtual environment
python -m venv files\venv
echo Activating the virtual environment
call files\venv\Scripts\activate.bat
echo Upgrading pip
python -m pip install --upgrade pip
echo Installing required packages inside the virtual environment
python -m pip install requests PyQt5
echo Setting UTF-8 encoding
set PYTHONIOENCODING=utf-8
echo Running generate_csv.py
python files\generate_csv.py
echo Running version_query.py
python files\version_query.py
echo Deactivating the virtual environment
call files\venv\Scripts\deactivate.bat
echo Deleting the virtual environment folder
rmdir /S /Q files\venv
echo Task completed. Exiting.
endlocal
