@ECHO OFF
TITLE windows-info v0.1
echo -------------------------机器名-------------------------
hostname
echo -------------------------用户信息-------------------------
net user
echo -------------------------在线用户-------------------------
query user
echo -------------------------正在连接的IP-------------------------
netstat -ano |findstr ESTABLISHED|findstr /v 127.0.0.1
echo -------------------------正在监听的端口-------------------------
netstat -ano |findstr LISTENING
echo -------------------------尝试备份安全日志到当前目录-------------------------
wevtutil epl Security %USERPROFILE%\desktop\Sec.evtx
echo -------------------------尝试获取远程登录日志-------------------------
wevtutil qe Security "/q:*[System [(EventID=4648)]]" /f:text /rd:true /c:10
echo -------------------------其他·提示-------------------------
echo 查询隐藏用户：HKEY_LOCAL_MACHINE --SAM–SAM(需要右击权限修改管理员权限)-Domains-Account-users
echo 查询密码信息：mimikatz privilege::debug sekurlsa::logonpasswords
echo 查询web浏览记录、浏览器密码、web日志导出
PAUSE