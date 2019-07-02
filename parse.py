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
#        print("http://localhost:9090/api/v1/query_range?query=node_cpu_seconds_total&start=%s&end=%s&step=5s" % (start.isoformat() + "Z", end.isoformat() + "Z"))
#        r = requests.get("http://localhost:9090/api/v1/query_range?query=node_cpu_seconds_total&mode=idle&start=%s&end=%s&step=15s" % (start.isoformat() + "Z", end.isoformat() + "Z"))
#        print(r.text)
        fres.write("%s,%s,%s,%d\n" %(from_format, size, acc,(end - start).seconds))


collect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

