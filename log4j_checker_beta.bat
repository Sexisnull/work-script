@echo off
tasklist |findstr /i java.exe && (goto:succeed) || (goto:failed)
:succeed
for /f "tokens=8 delims==" %%i in ('wmic process where name^="java.exe" get commandline ^|findstr /i tomcat') do (set ph=%%i)
set str=%ph:~1,-18%
set "str2=\webapps\"
set "str3=%str%%str2%"
echo "-----找到web路径-----"
echo %str3%
for /R %str3% %%f in (log4j*) do (echo "-----查找到存在log4j-----"&&echo "%%f"&&set "file=%%f")
IF [%file%]==[] echo "-----未查找到log4j-----"
pause
:failed
echo "未找到java应用"
pause
