from funcSteam import *
import var
import json
dstKill()
time.sleep(1)
steamKill()
time.sleep(1)

fds = sorted(os.listdir('./maFiles'))
for maf in fds:
    if maf.endswith(('.maFile')): 
        print('--------------------------------------------------')
        with open('./maFiles/'+str(maf), "r") as read_file:
            data = json.load(read_file)
            print(data["account_name"])
            runSteam(data["account_name"],var.Pass[data["account_name"]],data["shared_secret"])
            runDst()