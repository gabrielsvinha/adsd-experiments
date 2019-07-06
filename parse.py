from os import listdir
from os.path import isfile, join
from datetime import datetime, tzinfo, timedelta
import sys
import requests

class simple_utc(tzinfo):
    def tzname(self,**kwargs):
        return "UTC"
    def utcoffset(self, dt):
        return timedelta(0)

def collect(from_format, size, acc, rep):
    fres = open("results/2/raw-convert.csv", 'a')
    filename="logs/%s-%s-time.txt" %(size, rep)
    with open(filename, 'r') as f:
        lines = f.readlines()
        start = datetime.strptime(lines[0].split("\n")[0], '%y-%m-%d %H:%M:%S.%f')
        end = datetime.strptime(lines[1].split("\n")[0], '%y-%m-%d %H:%M:%S.%f')
        if (end-start).seconds < 5:
            r = requests.get('http://localhost:9090/api/v1/query?query=(1-avg+by+(instance)(rate(node_cpu_seconds_total{mode="idle"}[5s])))')
        else:
            r = requests.get('http://localhost:9090/api/v1/query?query=(1-avg+by+(instance)(rate(node_cpu_seconds_total{mode="idle"}[%ds])))' % (end-start).seconds)
        r2 = requests.get("http://localhost:9090/api/v1/query?query=(node_memory_MemTotal_bytes-avg_over_time(node_memory_MemFree_bytes[%ds]))/1000000" % max(1, (end-start).seconds))
        print(r.url)
        print(r.json())
        print(max(5, (end-start).seconds))
        cpu = r.json()['data']['result'][0]['value'][1]
        mem = r2.json()['data']['result'][0]['value'][1]
        fres.write("%s,%s,%s,%d,%s,%s\n" %(from_format, size, acc,(end - start).total_seconds(), cpu, mem))


collect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

