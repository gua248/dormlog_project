from hdfs.client import *
import re
import time
from hdfs.util import HdfsError

client = Client("http://node3:9870", root='/')


def hdfs_write_append(path, data):
    try:
        client.write(path, data, append=True)
    except HdfsError:
        client.write(path, data, overwrite=True)


data = '\n' + '*'*20 + ' STAT @ ' + time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime())
print(data, end='')
hdfs_write_append('/dormlog_project/stat_bytes.txt', data=data)

with client.read('/dormlog_project/result_bytes.txt') as f:
    content = f.readlines()
    tot_bytes = 0
    for line in content:
        line = line.decode()
        b = re.search(r'--- *(\d+) bytes', line)
        b = 0 if b is None else int(b.groups()[0])
        tot_bytes += b
    data = '*' * 20 + ' {:>12d} bytes\n'.format(tot_bytes)
    print(data, end='')
    hdfs_write_append('/dormlog_project/stat_bytes.txt', data=data)

for name in ['ip', 'device', 'status']:
    path = '/dormlog_project/stat_' + name + '.txt'
    data = '\n' + '*' * 20 + ' STAT @ ' + time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime())
    print(data, end='')
    hdfs_write_append(path, data=data)

    with client.read('/dormlog_project/result_' + name + '.txt') as f:
        content = f.readlines()
        tot_cnt = {}
        for line in content:
            line = line.decode()
            b = re.match(r'\(\'(.+)\', (\d+)\)', line)
            if b is not None:
                key, val = b.groups()
                if key in tot_cnt:
                    tot_cnt[key] += int(val)
                else:
                    tot_cnt[key] = int(val)
        if name in ['device', 'status']:
            for kv in sorted(tot_cnt.items()):
                data = '*' * 20 + ' ' + str(kv) + '\n'
                print(data, end='')
                hdfs_write_append(path, data=data)
        else:  # ip
            data = '*' * 20 + ' TOP 10 IPs\n'
            hdfs_write_append(path, data=data)
            ip_list = sorted(tot_cnt.items(), key=lambda x: x[1], reverse=True)
            n = min(len(ip_list), 10)
            for kv in ip_list[:n]:
                data = '*' * 20 + ' ' + str(kv) + '\n'
                print(data, end='')
                hdfs_write_append(path, data=data)
