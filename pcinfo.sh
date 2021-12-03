#! /bin/bash
# linux-info v0.2
# by: kid

echo "-------------------------机器名-------------------------"
hostname
echo "-------------------------查看用户信息-------------------------"
cat /etc/passwd |grep -v nologin |grep -v /bin/false
echo "-------------------------查看用户公钥信息-------------------------"
cat /root/.ssh/authorized_keys
echo "-------------------------查看用户目录信息-------------------------"
ls -al /home
echo "-------------------------查看登录信息-------------------------"
w
echo "-------------------------查看历史登录信息-------------------------"
last -F -n 10
echo "-------------------------查看安全日志中登录成功信息-------------------------"
grep "Accepted " /var/log/secure | awk '{print $1,$2,$3,$9,$11}'
grep "Accepted " /var/log/auth.log | awk '{print $1,$2,$3,$9,$11}'
echo "-------------------------查看历史命令，查找外联-------------------------"
cp /root/.bash_history history.b && echo "history文件已备份"
cat history.b |grep -E "([0-9]{1,3}[\.]){3}[0-9]{1,3}"
echo "-------------------------查看计划任务-------------------------"
crontab -l
echo "-------------------------查看CPU占用高的程序-------------------------"
ps -eo pid,ppid,%mem,%cpu,cmd --sort=-%cpu | head
echo "-------------------------查找恶意程序-------------------------"
evalpid=$(ps -eo pid,ppid,%mem,%cpu,cmd --sort=-%cpu | head -n 2|awk 'NR==2 {print $1}')
ls -al /proc/$evalpid |grep -E "cwd|exe"
echo "-------------------------查看正在连接的IP-------------------------"
netstat -antlp |grep ESTABLISHED
echo "-------------------------查看对外监听的端口-------------------------"
netstat -antlp |grep LISTEN | grep -v 127.0.0.1
echo "-------------------------查找隐藏文件-------------------------"
find /root/* /tmp/* /home/* -name ".*" -print |more
echo "-------------------------其他·提示-------------------------"
echo "查看用户进程：lsof -u hack"
echo "查看端口占用：lsof -i:8888"
