pyinstaller .\app\app.py^
 --onefile^
 --add-data "./app/data/.gitkeep;data/.gitkeep"^
 --add-data "./app/images/*;images"^
 --add-data "./app/resources/*;resources"
pyinstaller app.spec
