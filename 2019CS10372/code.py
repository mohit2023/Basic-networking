import sys
import subprocess
import matplotlib.pyplot as plt

def ping(host, ttl):
  param1 = '-n'
  param2 = '-i'
  command = ['ping', param1, '1', param2, str(ttl), host]
  res = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8')
  return res

def rttValue(res):
  res = res[res.index('Average = ') + 10:]
  res = res[0:res.index('ms')]
  return int(res)

def ipValue(res):
  res = res.split('\n')
  start = 11
  end = res[2].index(':')
  ip = res[2][start:end]
  return ip

def roundTripTime(ip):
  res = ping(ip,100)
  if 'Request timed out' in res:
    return 0
  return rttValue(res)

def hop(host, i):
  res = ping(host, i)
  if 'TTL expired in transit' in res:
    ip = ipValue(res)
    rtt = roundTripTime(ip)
    return ip,rtt,False
  elif 'Request timed out' in res:
    return '*',0,False
  else:
    ip = ipValue(res)
    rtt = rttValue(res)
    return ip,rtt,True

def tracert(host, max_hops):
  arr = []
  x = []
  y = []
  for i in range(1,max_hops+1):
    ip,rtt,end = hop(host,i)
    x.append(i)
    y.append(rtt)
    arr.append([i,ip,rtt])
    if end:
      break
  return x,y,arr

def assignment(host):
  x,y,arr = tracert(host, 30)
  plt.plot(x,y)
  plt.xlabel('Hope Number')
  plt.ylabel('Round Trip Time(ms)')
  plt.title('RTT VS Hop')
  plt.show()
  print('tracert using ping for ', host, '\n')
  print('Hop \t RTT \t IP Address\n')
  for item in arr:
    print(item[0], '\t', item[2], '\t', item[1])

args = sys.argv
host = args[1]
# host = "www.iitd.ac.in"
assignment(host)

