@echo off
if "%1" == "-d" (
 set USE_CONSOLE=
) else (
 set USE_CONSOLE="--noconsole"
)
@echo on

pyinstaller .\app\app.py^
 --name "Maze"^
 --noconfirm^
 %USE_CONSOLE%^
 --add-data "./app/data/.gitkeep;data/.gitkeep"^
 --add-data "./app/images/*;images"^
 --add-data "./app/resources/*;resources"^
 --icon "./app/images/icon.png"^
 --clean

@echo off
if %errorlevel% neq 0 goto EOF
@echo on

tar^
 -c^
 -v^
 -f "dist\maze_0.0.1.zip"^
 -C .\dist^
  "Maze"

@echo off
if %errorlevel% neq 0 goto EOF
@echo on

.\dist\Maze\Maze.exe

:EOF
@echo on
