@ECHO OFF
TITLE windows-info v0.1
echo -------------------------������-------------------------
hostname
echo -------------------------�û���Ϣ-------------------------
net user
echo -------------------------�����û�-------------------------
query user
echo -------------------------�������ӵ�IP-------------------------
netstat -ano |findstr ESTABLISHED|findstr /v 127.0.0.1
echo -------------------------���ڼ����Ķ˿�-------------------------
netstat -ano |findstr LISTENING
echo -------------------------���Ա��ݰ�ȫ��־����ǰĿ¼-------------------------
wevtutil epl Security %USERPROFILE%\desktop\Sec.evtx
echo -------------------------���Ի�ȡԶ�̵�¼��־-------------------------
wevtutil qe Security "/q:*[System [(EventID=4648)]]" /f:text /rd:true /c:10
echo -------------------------��������ʾ-------------------------
echo ��ѯ�����û���HKEY_LOCAL_MACHINE --SAM�CSAM(��Ҫ�һ�Ȩ���޸Ĺ���ԱȨ��)-Domains-Account-users
echo ��ѯ������Ϣ��mimikatz privilege::debug sekurlsa::logonpasswords
echo ��ѯweb�����¼����������롢web��־����
PAUSE