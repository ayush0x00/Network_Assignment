import os
import subprocess
import matplotlib.pyplot as plt
from controller import plotMap

servers = ["gateway.iitmandi.ac.in","moneycontrol.com","harvard.edu"]


for server in servers:
    print(f"Plotting for {server}")
    delay = []
    throughPut = []
    for i in range(10):
        packetsToSend = 3
        res = subprocess.Popen(f'ping -c {packetsToSend} {server}', shell = True, stdout=subprocess.PIPE).stdout
        output = res.read()
        data = output.decode().split('\n')
        avgRTT = float(data[-2].split()[3].split('/')[1])/1000
        delay.append((avgRTT))
        throughPut.append((packetsToSend*64)/avgRTT)

    normDelay = [x/max(delay) for x in delay]
    normThrough = [x/max(throughPut) for x in throughPut]
    plt.plot(normThrough,normDelay,label=server)

plt.title("Evening session")
plt.xlabel("Throughput in Bps")
plt.ylabel("Delay in seconds")
plt.legend()
plt.show()

for server in servers:
    plotMap(server)

