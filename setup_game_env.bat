@chcp 65001 > nul
@echo off
echo [1/4] Проверка Python ...
python --version || (
    echo Python не найден. Установите Python 
    pause
    exit /b
)

echo [2/4] Обновление pip ...
python -m pip install --upgrade pip

echo [3/4] Установка зависимостей 
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo Файл не найден ...
    pause
    exit /b
)

echo [4/4] Установка завершена!
pause