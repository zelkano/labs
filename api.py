exec(open('0_global_vars.py').read())

uzn = input("Enter Username:")
paz = getpass.getpass("Enter Password:")

auth_to_encode = f"{uzn}:{paz}"
b64_auth = base64.b64encode(auth_to_encode.encode()).decode()
basic = f"Basic {b64_auth}"

f5_authheader = {'Content-Type': 'application/json','Authorization' : basic}

## connect and get the virtual servers

output = requests.get("https://bigip-b.example.net/mgmt/tm/gtm/server",headers=f5_authheader,verify=False)
outs = output.json()
servers = json.dumps(outs, indent=4)

## count how many GTM servers there are
numserv = len(outs['items'])
print(f'there are {numserv} Servers found on the GTM')

aa = input("press any key to continue..\n")

for x in outs['items']:
    servName = x['name']
    servProduct = x['product']
    a23 = x['datacenter']
    servDC = a23.strip('/Common/')

    print("-----------------------------\n")
    print(f"NAME:    {servName} \nPRODUCT: {servProduct} \nDC:      {servDC}")

    
    ### conenct to the GTM Server and list out its Virtual Servers
    outputvs = requests.get(f"https://bigip-b.example.net/mgmt/tm/gtm/server/~Common~{servName}/virtual-servers",headers=f5_authheader,verify=False)
    outsvs = outputvs.json()
    vslist = json.dumps(outsvs, indent=4)

    numvs = len(outsvs['items'])

    print(f'\nthere are {numvs} Servers found on {servName}\n')

    aa = input("press any key to View Virtual Servers..\n")

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


        print(f'Name: {vsName}:{vsDest}\nMonitor: {vsMon}')

    #print(vslist)

print("-----------------------------\n")

