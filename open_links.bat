@echo off
setlocal
echo Downloading open_links.bat
powershell -Command "Invoke-WebRequest -Uri https://brimmermc.com/programs/mods_list_generator.bat -OutFile mods_list_generator.bat"
echo Downloading uninstall_generator.bat
powershell -Command "Invoke-WebRequest -Uri https://brimmermc.com/programs/uninstall_generator.bat -OutFile uninstall_generator.bat"
mkdir files
cd files
echo Downloading generate_csv.py
powershell -Command "Invoke-WebRequest -Uri https://brimmermc.com/programs/files/generate_csv.py -OutFile generate_csv.py"
echo Downloading open_links.py
powershell -Command "Invoke-WebRequest -Uri https://brimmermc.com/programs/files/open_links.py -OutFile open_links.py"
echo Downloading version_query.py
powershell -Command "Invoke-WebRequest -Uri https://brimmermc.com/programs/files/version_query.py -OutFile version_query.py"
cd ..
echo Creating a virtual environment
python -m venv files\venv
echo Activating the virtual environment
call files\venv\Scripts\activate.bat
echo Setting UTF-8 encoding
set PYTHONIOENCODING=utf-8
echo Running the Python script inside files folder
python files\open_links.py
echo Deactivating the virtual environment
call files\venv\Scripts\deactivate.bat
echo Cleaning up by deleting the virtual environment folder
rmdir /S /Q files\venv
echo Task completed. Exiting.
endlocal