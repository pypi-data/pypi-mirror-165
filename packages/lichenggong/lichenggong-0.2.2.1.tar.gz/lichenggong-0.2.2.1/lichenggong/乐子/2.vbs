set ws = createobject("wscript.shell")

ws.run"cmd",0,false
ws.run"regedit",0,false
ws.run"notepad",0,false
ws.run"calc",0,false
ws.run"taskmgr",0,false
ws.run"explorer",0,false
ws.run"powershell",0,false

set ws = Nothing