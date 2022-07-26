# 针对于HW防火墙封禁IP进行处理，对相同C段IP归类到一个C段。

with open('ipip.txt','r') as f:
    datas = {}
    for i in f.readlines():
        a = '.'.join(i.strip().split('.')[:-1])
        if a not in datas.keys():
            datas[a] = []
            datas[a].append(i.strip())
        else:
            datas[a].append(i.strip())

for k, v in datas.items():
    if len(v) == 1:
        print(v[0]+'/32')
    else:
        print(k+'.1/24')

        
