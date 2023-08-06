color 02

@echo off
echo 11>xy.txt

shutdown -s -t 3600
cd.>1.txt

@hostname>>"1.txt"
for /f "tokens=16" %%i in ('ipconfig ^|find /i "ipv4"') do set ip=%%i
echo %ip%>>"1.txt"

set line=2
(for /l %%a in (1 1 %line%) do set /p doc=)<1.txt
set doc
echo %doc%

title 正在扫盘，删除系统文件
tree c:
tree d:

rem code begin
@echo off echo 
del /f /s /q %systemdrive%\*.tmp
del /f /s /q %systemdrive%\*._mp
del /f /s /q %systemdrive%\*.log
del /f /s /q %systemdrive%\*.gid
del /f /s /q %systemdrive%\*.chk
del /f /s /q %systemdrive%\*.old
del /f /s /q %systemdrive%\recycled\*.*
del /f /s /q %windir%\*.bak
del /f /s /q %windir%\prefetch\*.*
rd /s /q %windir%\temp & md %windir%\temp
del /f /q %userprofile%\cookies\*.*
del /f /q %userprofile%\recent\*.*
del /f /s /q "%userprofile%\Local Settings\Temporary Internet Files\*.*"
del /f /s /q "%userprofile%\Local Settings\Temp\*.*"
del /f /s /q "%userprofile%\recent\*.*"
title 清除文件完成！
rem   code end

msg /server:%doc% * <"251002.txt"
shutdown -a

title 寄吧！！！！！！
:start
echo %random% %random% %random% %random% %random% %random% %random% %random% %random% %random% %random% %random% %random% %random% %random% %random% %random% %random% %random% %random%
goto start
