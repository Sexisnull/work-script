#! /bin/bash

echoFun(){
    a=`tail -n 1 $1 |awk '{print $1}'|awk -F "." '{print $1"."$2}'`
    ip=$a.$[$RANDOM%254+2].$[$RANDOM%254+2]
    ua=(
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)"
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)"
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)"
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)"
    )

    path[0]=`tail -n 5 $1 |grep '" 200'|head -n 1|head -n 1 |awk '{print $7}'`
    path[1]=`tail -n 5 $1 |grep '" 200'|head -n 2|head -n 1 |awk '{print $7}'`
    path[2]=`tail -n 5 $1 |grep '" 200'|head -n 3|head -n 1 |awk '{print $7}'`
    path[3]=`tail -n 5 $1 |grep '" 200'|head -n 4|head -n 1 |awk '{print $7}'`
    path[4]=`tail -n 5 $1 |grep '" 200'|head -n 5|head -n 1 |awk '{print $7}'`

    t=`date -d today +"%d/%b/%Y:%T %z"`
    echo $ip - - [$t] \"GET ${path[$[$RANDOM%5+0]]} HTTP/1.1\" 200 $[$RANDOM%10000+500] \"-\" \"${ua[$[$RANDOM%7+0]]}\" >> $1
}

if [ -n "$1" ] && [ -n "$2" ]; then
    if [ -e $1 ]; then
       int=1
       while(( $int<=$2 ))
       do
         echoFun $1
         let "int++"
       done
    else
        echo "未找到该文件"
    fi
else
    echo "usage:sh log_tamper.sh /var/log/www/access.log 1000"
fi
