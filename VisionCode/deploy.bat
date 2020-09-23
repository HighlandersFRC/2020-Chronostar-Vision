taskkill /IM obs64.exe /f
taskkill /IM putty.exe /f
taskkill /IM plink.exe /f

set "MODULE_NAME=TapeDetectCody"
set "COM_PORT=COM14"

cd "C:\Users\Cody1\Desktop\Highlanders\2019-Gravastar\VisionCode"
start /b plink.exe -load %COM_PORT% < mountJevois.txt

sleep 10

taskkill /IM plink.exe /f

set "FROM_FILE=modules\Highlanders\%MODULE_NAME%\%MODULE_NAME%.py"
set "TO_FILE=D:\modules\Highlanders\%MODULE_NAME%\"
cp %FROM_FILE% %TO_FILE%

set "FROM_FILE=modules\Highlanders\%MODULE_NAME%\script.cfg"
cp %FROM_FILE% %TO_FILE%

set "FROM_FILE=config\initscript.cfg"
set "TO_FILE=D:\config\"
cp %FROM_FILE% %TO_FILE%

set "FROM_FILE=config\videomappings.cfg"
cp %FROM_FILE% %TO_FILE%

dir %TO_FILE%

sleep 5

start /b plink.exe -load %COM_PORT% < restartJevois.txt
taskkill /IM plink.exe /f

sleep 15

cd "C:\Users\Cody1\Desktop"
start /b putty.exe -load COM14

cd "C:\Program Files\obs-studio\bin\64bit"
start /b obs64.exe

