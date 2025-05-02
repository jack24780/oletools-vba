@echo off
echo 安装VBA解密工具所需依赖...
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo 安装失败，请确保已安装Python和pip
    pause
    exit /b 1
)

echo 安装完成!
echo 你可以使用以下命令分析VBA加密文档:
echo.
echo python vba_analyzer.py 你的文件.doc -c
echo 或
echo python vba_password.py 你的文件.doc
echo.
pause