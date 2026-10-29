@echo off
rem Instala o Flask (se precisar) e liga o servidor do EntreFrames.
cd /d "%~dp0"
python -m pip install -q -r requirements.txt
if errorlevel 1 (
  echo.
  echo Nao foi possivel instalar o Flask. Verifique se o Python esta instalado.
  pause
  exit /b 1
)
echo.
echo Baixando os posteres que faltam...
python baixar_posteres.py
echo.
echo Abra http://127.0.0.1:5000 no navegador. Para desligar, feche esta janela.
echo.
python app.py
pause
