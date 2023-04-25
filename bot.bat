@ECHO OFF
pip install --user -r requirements.txt
CLS
CD %~dp0
python app.py
PAUSE