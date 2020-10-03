import requests
import json
import matplotlib.pyplot as plt
API_URL = "https://censys.io/api/v1/search/ipv4"
UID = "Enter Your UID Here"
SECRET = "Enter Your Secret Here"
data = '{ "query": "ip: 152.1.0.0/16 ", "flatten": true, "fields": ["ip", "80.http.get.headers.server", "protocols", "metadata.os"]}'
res = requests.post(API_URL, headers = {"Content-Type": "application/json"}, auth=(UID, SECRET), data= data)
jsn = json.loads(res.content.decode("utf-8"))
for k, v in jsn.items():
  if k == "results":
    a = v
text_file = open("Output.txt", "w")
ipcount = 0
z = []
prot = []
server = []
oscount = {'Windows':0, 'Ubuntu':0, 'Unix':0, 'Fedora':0, 'Raspbian':0, 'Unknown':0}
protocols_ = {}
servers_ = {}
for i in a:
  for x,v in i.items():
    #print(x)
    if x == 'ip':   #Output.txt saves all the hosts available
      text_file.write(v)
      text_file.write(', ')
      text_file.write('\n')
      ipcount +=1

    if x == 'metadata.os':
      z.append(v)
    if x == '80.http.get.headers.server':
      server.append(v)
    if x == 'protocols':
      prot.extend(v)


for key in z:                     #os count from list to dictionary
  oscount[key]+=1
for new in server:                #server count from list to dictionary
  if new in servers_:
    servers_[new]+=1
  else:
    servers_[new] = 1

for pr in prot:               #protocols count from list to dictionary
  if pr in protocols_:
    protocols_[pr] +=1
  else:
    protocols_[pr] =1
print(ipcount)



## Plot graphs using Matplotlib library ##
plt.figure('Operating Systems')   ##OS
oscount['Unknown'] = ipcount - sum(oscount.values())
hosts = oscount.values()
os = oscount.keys()
plt.bar(os, hosts, color = 'teal')
plt.xlabel('Operating System')
plt.ylabel('Number of Hosts')
plt.show()

plt.figure('Webservers')             ##Webservers
webservers = servers_.keys()
hosts_ = servers_.values()
plt.bar(webservers, hosts_, color = 'green')
plt.xlabel('Webservers')
plt.ylabel('Hosts')
plt.show()

plt.figure('Protocols')         #Protocols
#print(servers_)
nameofprot = protocols_.keys()
noofprot = protocols_.values()
plt.bar(nameofprot, noofprot, color = 'yellow')
plt.xlabel('Name of protocol')
plt.ylabel('Number of hosts')
plt.show()


plt.figure('Total number of hosts in the two CIDR block')
newdict = {'152.1.0.0/16': 100, '192.58.122.0/24':5}
plt.bar(newdict.keys(), newdict.values(), color = 'orange')
plt.xlabel('CIDR Block')
plt.ylabel('Total number of hosts')
plt.show()
