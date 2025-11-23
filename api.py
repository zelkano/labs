exec(open('0_global_vars.py').read())

poolandmember={}
serverandvirtual={}

uzn = input("Enter Username:")
paz = getpass.getpass("Enter Password:")

auth_to_encode = f"{uzn}:{paz}"
b64_auth = base64.b64encode(auth_to_encode.encode()).decode()
basic = f"Basic {b64_auth}"

f5_authheader = {'Content-Type': 'application/json','Authorization' : basic}

## connect and get the Pools

print("\nGathering Pools and Pool Members\n")

outpool = requests.get("https://bigip-b.example.net/mgmt/tm/gtm/pool/a/",headers=f5_authheader,verify=False)
jspool = outpool.json()
pools = json.dumps(jspool, indent=4)
pool = jspool['items']

for t in pool:
    #print(t['name'])
    outmems = requests.get(f"https://bigip-b.example.net/mgmt/tm/gtm/pool/a/~Common~{t['name']}/members",headers=f5_authheader,verify=False)
    jsmems = outmems.json()
    membs = json.dumps(jsmems, indent=4)
    members = jsmems['items']

    memlist = []

    for xy in members:
        memname = xy['name']
        #print(f'Name: {memname}')
        memlist.append(memname)
    

    poolandmember[t['name']] = {"Members" : memlist}

print("done!\n")
""" 
#print(pools)

print("\n\n---\n")

for i in poolandmember:

    print(poolandmember[i]['Members'][0])

"""

## connect and get the virtual servers
print("\nGathering GTM Servers and Virtual Servers\n")

output = requests.get("https://bigip-b.example.net/mgmt/tm/gtm/server",headers=f5_authheader,verify=False)
outs = output.json()
servers = json.dumps(outs, indent=4)

## count how many GTM servers there are
numserv = len(outs['items'])

#print(f'there are {numserv} Servers found on the GTM')


for x in outs['items']:
    servName = x['name']
    servProduct = x['product']
    a23 = x['datacenter']
    servDC = a23.lstrip('/')
    servDC = servDC.lstrip('Common')
    servDC = servDC.lstrip('/')

    #print("-----------------------------\n")
    #print(f"NAME:    {servName} \nPRODUCT: {servProduct} \nDC:      {servDC}")

    
    ### conenct to the GTM Server and list out its Virtual Servers
    outputvs = requests.get(f"https://bigip-b.example.net/mgmt/tm/gtm/server/~Common~{servName}/virtual-servers",headers=f5_authheader,verify=False)
    outsvs = outputvs.json()
    vslist = json.dumps(outsvs, indent=4)

    numvs = len(outsvs['items'])

    #print(f'\nthere are {numvs} Virtual Servers found on {servName}\n')

    
    servlist=[]

    for tt in outsvs['items']:
        vsName = tt['name']
        vsDest = tt['destination']

        if tt.get('monitor') is None:
            vsMon = "None"
        else:
            vsMon = tt['monitor']
            vsMon = vsMon.lstrip('/')
            vsMon = vsMon.lstrip('Common')
            vsMon = vsMon.lstrip('/')


        #print(f'Name: {vsName}:{vsDest}\nMonitor: {vsMon}')
        servlist.append(vsName)

    serverandvirtual[servName] = {'Members' : servlist}

    #print(vslist)

print("-----------------------------\n")
print("searching for Virtual Servers which do not exist in Pools\n")

for i in serverandvirtual:
    #print(f"{i} -- {serverandvirtual[i]['Members']}")
    
    for x in serverandvirtual[i]['Members']:
        found = False
        #print(f"searchign for {x}")

        for k in poolandmember:
            #print(f"{i} -- {poolandmember[i]['Members']}")

            for y in poolandmember[k]['Members']:
                if found == True:
                    break
                else:
                    if x in y:
                        #print(f"Server found in pool {k}")
                        found = True
                        break
            

        if found == False:
            print(f"Virtual Server {i}:{x} - not found in any pools")

    
quit()

print("\n---------\n")

for i in poolandmember:
    print(f"{i} -- {poolandmember[i]['Members']}")
    for x in poolandmember[i]['Members']:
        print(x)

